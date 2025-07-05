"""
聊天处理逻辑
"""

import requests
import re
from typing import List, Tuple
from config import OLLAMA_URL, MODEL_NAME, GENERATION_CONFIG


class ChatHandler:
    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.model_name = MODEL_NAME
        self.generation_config = GENERATION_CONFIG

    def chat_with_ollama(self, message: str, history: List[Tuple[str, str]]) -> str:
        """与Ollama模型对话"""
        try:
            # 构建上下文
            context = ""
            for user_msg, bot_msg in history:
                context += f"用户: {user_msg}\n助手: {bot_msg}\n"

            full_prompt = f"{context}用户: {message}\n助手: "

            # 调用Ollama API
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": self.generation_config
            }

            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                bot_response = result.get("response", "抱歉，我没有收到有效的响应。")
                return bot_response.strip()
            else:
                return f"错误：无法连接到Ollama服务 (状态码: {response.status_code})"

        except requests.exceptions.RequestException as e:
            return f"连接错误：{str(e)}"
        except Exception as e:
            return f"发生错误：{str(e)}"

    def parse_response(self, response: str) -> Tuple[str, str]:
        """解析响应，分离思考过程和最终内容"""
        # 查找 <think> 标签
        think_pattern = r'<think>(.*?)</think>'
        think_match = re.search(think_pattern, response, re.DOTALL)

        if think_match:
            # 提取思考过程
            think_content = think_match.group(1).strip()
            # 提取正文内容（移除 <think> 标签后的剩余内容）
            main_content = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()

            # 格式化完整的显示内容
            display_content = f"""**🤔 思考过程：**

{think_content}

---

**💡 回答：**

{main_content}"""

            return display_content, main_content
        else:
            # 没有思考标签，直接返回原内容
            return response, response

    def process_message(self, message: str, history: List[Tuple[str, str]]) -> Tuple[str, str]:
        """处理消息并返回显示内容和TTS内容"""
        if not message.strip():
            return "", ""

        # 获取机器人响应
        raw_response = self.chat_with_ollama(message, history)

        # 解析响应，分离思考过程和正文
        display_content, tts_content = self.parse_response(raw_response)

        return display_content, tts_content