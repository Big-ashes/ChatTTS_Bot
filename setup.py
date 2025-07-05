#!/usr/bin/env python3
"""
AI聊天助手安装脚本
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path


def create_directories():
    """创建必要的目录"""
    dirs = ['assets', 'audio_output', 'utils']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ 创建目录完成")


def install_dependencies():
    """安装Python依赖"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败，请手动运行: pip install -r requirements.txt")


def download_sample_avatars():
    """下载示例头像（可选）"""
    print("📥 准备下载示例头像...")

    # 这里可以添加实际的头像下载逻辑
    # 目前创建占位文件
    avatar_files = [
        "assets/bot_avatar.png",
        "assets/user_avatar.png"
    ]

    for avatar_file in avatar_files:
        if not os.path.exists(avatar_file):
            # 创建占位文件提示
            with open(avatar_file + ".placeholder", "w") as f:
                f.write(f"请将64x64像素的PNG头像文件重命名为: {os.path.basename(avatar_file)}")

    print("💡 请手动添加头像文件到assets/目录")


def check_services():
    """检查必要服务"""
    print("🔍 检查服务状态...")

    # 检查Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama服务正常")
        else:
            print("⚠️ Ollama服务异常")
    except:
        print("❌ Ollama服务未启动，请运行: ollama serve")

    # 检查ChatTTS
    try:
        response = requests.post(
            "http://localhost:8000/v1/audio/speech",
            json={"model": "tts-1", "input": "test", "voice": "echo"},
            headers={"Content-Type": "application/json", "Authorization": "Bearer sk-xxx"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ ChatTTS服务正常")
        else:
            print("⚠️ ChatTTS服务异常")
    except:
        print("❌ ChatTTS服务未启动，请启动ChatTTS服务")


def main():
    """主安装流程"""
    print("🚀 AI聊天助手安装脚本")
    print("=" * 50)

    # 创建目录
    create_directories()

    # 安装依赖
    install_dependencies()

    # 下载示例头像
    download_sample_avatars()

    # 检查服务
    check_services()

    print("\n" + "=" * 50)
    print("🎉 安装完成！")
    print("\n📋 接下来的步骤:")
    print("1. 启动Ollama服务: ollama serve")
    print("2. 启动ChatTTS服务")
    print("3. 添加头像文件到assets/目录")
    print("4. 运行程序: python app.py")
    print("5. 访问: http://localhost:7860")


if __name__ == "__main__":
    main()