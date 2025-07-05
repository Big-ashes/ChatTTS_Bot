"""
语音合成处理
"""

import requests
import time
import os
from config import CHATTTS_URL, TTS_CONFIG, TTS_HEADERS


class TTSHandler:
    def __init__(self):
        self.chattts_url = CHATTTS_URL
        self.tts_config = TTS_CONFIG
        self.headers = TTS_HEADERS

    def text_to_speech(self, text: str) -> str:
        """调用ChatTTS进行语音合成"""
        try:
            if not text.strip():
                return None

            payload = {
                **self.tts_config,
                "input": text
            }

            response = requests.post(
                self.chattts_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                # 创建音频文件目录
                os.makedirs("audio_output", exist_ok=True)

                # 保存音频文件
                audio_filename = f"audio_output/output_{int(time.time())}.mp3"
                with open(audio_filename, "wb") as f:
                    f.write(response.content)
                return audio_filename
            else:
                print(f"TTS错误：状态码 {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"TTS连接错误：{str(e)}")
            return None
        except Exception as e:
            print(f"TTS发生错误：{str(e)}")
            return None

    def cleanup_old_audio(self, max_files=10):
        """清理旧的音频文件，保留最新的几个"""
        try:
            audio_dir = "audio_output"
            if not os.path.exists(audio_dir):
                return

            files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
            files.sort(key=lambda x: os.path.getctime(os.path.join(audio_dir, x)))

            # 删除多余的文件
            if len(files) > max_files:
                for file in files[:-max_files]:
                    try:
                        os.remove(os.path.join(audio_dir, file))
                    except:
                        pass
        except Exception as e:
            print(f"清理音频文件时出错：{str(e)}")