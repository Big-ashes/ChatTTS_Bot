"""
AI聊天助手主程序
"""

import gradio as gr
import requests
import os
from typing import List, Tuple
from utils import ChatHandler, TTSHandler
from config import (
    OLLAMA_TAGS_URL, CHATTTS_URL, MODEL_NAME, INTERFACE_CONFIG,
    get_avatar_path, TTS_CONFIG, TTS_HEADERS
)


class ChatInterface:
    def __init__(self):
        self.chat_handler = ChatHandler()
        self.tts_handler = TTSHandler()

    def chat_response(self, message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """处理聊天响应"""
        if not message.strip():
            return history, None

        # 获取处理后的内容
        display_content, tts_content = self.chat_handler.process_message(message, history)

        # 更新历史记录
        history.append((message, display_content))

        # 生成语音（只使用正文内容）
        audio_file = self.tts_handler.text_to_speech(tts_content)

        # 清理旧音频文件
        self.tts_handler.cleanup_old_audio()

        return history, audio_file


def create_interface():
    """创建Gradio界面"""
    chat_interface = ChatInterface()

    # 获取头像路径
    bot_avatar = get_avatar_path("bot")
    user_avatar = get_avatar_path("user")

    with gr.Blocks(
        title="AI聊天助手",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .chat-message {
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
        }
        .chatbot .message {
            max-width: 85%;
            line-height: 1.6;
        }
        .chatbot .message.bot {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
        }
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
        }
        """
    ) as demo:

        gr.Markdown(
            """
            # 🤖 AI聊天助手

            基于本地Ollama DeepSeek-R1模型和ChatTTS语音合成

            **功能特点：**
            - 💬 文字对话：使用DeepSeek-R1:8b模型，显示完整思考过程
            - 🔊 语音合成：ChatTTS生成语音回复（仅朗读正文内容）
            - 🧠 思考展示：可视化AI的推理过程
            - 🖼️ 个性化头像：用户和机器人头像
            - 📱 响应式界面：支持多设备访问
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                # 聊天界面
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    bubble_full_width=False,
                    height=600,
                    show_label=False,
                    avatar_images=(user_avatar, bot_avatar),
                    render_markdown=True
                )

                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="在这里输入您的消息...",
                        show_label=False,
                        scale=4,
                        container=False
                    )
                    send_btn = gr.Button("发送 📤", variant="primary", scale=1)

                with gr.Row():
                    clear_btn = gr.Button("清除历史 🗑️", variant="secondary")

            with gr.Column(scale=1):
                # 语音输出区域
                gr.Markdown("### 🔊 语音输出")
                audio_output = gr.Audio(
                    label="AI语音回复",
                    autoplay=True,
                    show_download_button=True
                )

                # 系统状态
                gr.Markdown("### 📊 系统状态")
                status_text = gr.Textbox(
                    value="系统初始化中...",
                    label="状态",
                    interactive=False
                )

                # 设置区域
                gr.Markdown("### ⚙️ 设置")
                with gr.Accordion("高级设置", open=False):
                    model_info = gr.Textbox(
                        value=MODEL_NAME,
                        label="当前模型",
                        interactive=False
                    )
                    ollama_status = gr.Textbox(
                        value="localhost:11434",
                        label="Ollama地址",
                        interactive=False
                    )
                    tts_status = gr.Textbox(
                        value="localhost:8000/v1/audio/speech",
                        label="ChatTTS地址",
                        interactive=False
                    )

                # 头像状态
                gr.Markdown("### 🖼️ 头像状态")
                avatar_status = gr.Textbox(
                    value=f"用户: {user_avatar}\n机器人: {bot_avatar}",
                    label="头像文件",
                    interactive=False,
                    lines=2
                )

        # 事件处理
        def respond(message, history):
            """处理用户消息"""
            try:
                new_history, audio = chat_interface.chat_response(message, history)
                return new_history, "", audio, "✅ 响应生成成功"
            except Exception as e:
                return history, message, None, f"❌ 错误：{str(e)}"

        def clear_history():
            """清除聊天历史"""
            return [], "🗑️ 历史记录已清除"

        # 绑定事件
        msg.submit(
            respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg, audio_output, status_text]
        )

        send_btn.click(
            respond,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg, audio_output, status_text]
        )

        clear_btn.click(
            clear_history,
            outputs=[chatbot, status_text]
        )

        # 启动时检查服务状态
        def check_services():
            """检查服务状态"""
            status_messages = []

            try:
                # 检查Ollama
                ollama_response = requests.get(OLLAMA_TAGS_URL, timeout=5)
                if ollama_response.status_code == 200:
                    status_messages.append("✅ Ollama服务正常")
                else:
                    status_messages.append("❌ Ollama服务异常")
            except:
                status_messages.append("❌ Ollama服务连接失败")

            try:
                # 检查ChatTTS
                test_payload = {**TTS_CONFIG, "input": "test"}
                chattts_response = requests.post(
                    CHATTTS_URL,
                    json=test_payload,
                    headers=TTS_HEADERS,
                    timeout=5
                )
                if chattts_response.status_code == 200:
                    status_messages.append("✅ ChatTTS服务正常")
                else:
                    status_messages.append("❌ ChatTTS服务异常")
            except:
                status_messages.append("❌ ChatTTS服务连接失败")

            # 检查头像文件
            if os.path.exists("assets/bot_avatar.png"):
                status_messages.append("✅ 机器人头像已加载")
            else:
                status_messages.append("⚠️ 机器人头像使用默认")

            if os.path.exists("assets/user_avatar.png"):
                status_messages.append("✅ 用户头像已加载")
            else:
                status_messages.append("⚠️ 用户头像使用默认")

            return " | ".join(status_messages)

        # 界面加载时检查服务
        demo.load(check_services, outputs=[status_text])

        # 添加示例
        gr.Examples(
            examples=[
                ["你好，请介绍一下你自己"],
                ["请解释一下人工智能的基本原理"],
                ["写一首关于春天的诗"],
                ["帮我制定一个学习计划"],
                ["什么是量子计算？"],
                ["请用简单的话解释相对论"],
                ["推荐几本好书"]
            ],
            inputs=[msg],
            label="💡 示例问题"
        )

        gr.Markdown(
            """
            ---

            **使用说明：**
            1. 确保Ollama服务运行在localhost:11434
            2. 确保ChatTTS服务运行在localhost:8000  
            3. 将头像文件放在assets/目录下（bot_avatar.png, user_avatar.png）
            4. 在文本框中输入消息，点击发送或按Enter键
            5. AI会显示完整的思考过程和最终回答
            6. 语音合成只会朗读正文内容，不包含思考过程

            **注意事项：**
            - 首次使用时可能需要下载模型，请耐心等待
            - 语音合成需要一定时间，请等待音频生成完成
            - 头像文件建议64x64像素PNG格式
            - 如果服务连接失败，请检查相关服务是否正常运行
            """
        )

    return demo


def main():
    """主函数"""
    # 创建必要的目录
    os.makedirs("assets", exist_ok=True)
    os.makedirs("audio_output", exist_ok=True)

    # 创建并启动界面
    demo = create_interface()

    print("🚀 启动AI聊天助手...")
    print(f"📝 Ollama模型: {MODEL_NAME}")
    print("🔊 TTS服务: ChatTTS (localhost:8000)")
    print("🌐 访问地址: http://localhost:7860")
    print("📁 项目目录结构:")
    print("  ├── assets/          # 头像文件")
    print("  ├── audio_output/    # 生成的音频文件")
    print("  └── utils/           # 工具模块")

    demo.launch(**INTERFACE_CONFIG)


if __name__ == "__main__":
    main()