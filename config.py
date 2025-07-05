"""
配置文件
"""

import os

# 服务器配置
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
CHATTTS_URL = "http://localhost:8000/v1/audio/speech"

# 模型配置
MODEL_NAME = "deepseek-r1:8b"

# 生成参数
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2000
}

# 界面配置
INTERFACE_CONFIG = {
    "server_name": "0.0.0.0",
    "server_port": 7860,
    "share": True,
    "debug": False,
    "show_error": True,
    "quiet": False
}

# 头像配置
BOT_AVATAR = "assets/bot_avatar.png"
USER_AVATAR = "assets/user_avatar.png"

# 检查头像文件是否存在
def get_avatar_path(avatar_type):
    """获取头像路径，如果文件不存在则返回默认emoji"""
    if avatar_type == "bot":
        return BOT_AVATAR if os.path.exists(BOT_AVATAR) else "🤖"
    elif avatar_type == "user":
        return USER_AVATAR if os.path.exists(USER_AVATAR) else "👤"
    else:
        return "❓"

# ChatTTS配置
TTS_CONFIG = {
    "model": "tts-1",
    "voice": "echo",
    "response_format": "mp3"
}

TTS_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-xxx"
}