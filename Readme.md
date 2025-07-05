# AI聊天助手项目

## 项目结构

```
ai-chat-assistant/
├── assets/
│   ├── bot_avatar.png          # 机器人头像 (64x64px)
│   └── user_avatar.png         # 用户头像 (64x64px)
├── app.py                      # 主程序文件
├── requirements.txt            # 依赖包列表
├── README.md                   # 项目说明
├── config.py                   # 配置文件
└── utils/
    ├── __init__.py
    ├── chat_handler.py         # 聊天处理逻辑
    └── tts_handler.py          # 语音合成处理
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动必要服务
- 确保 Ollama 服务运行在 `localhost:11434`
- 确保 ChatTTS 服务运行在 `localhost:8000`

### 3. 运行程序
```bash
python app.py
```

### 4. 访问界面
浏览器访问: `http://localhost:7860`

## 示例界面

![描述信息](/assets/webui.png)