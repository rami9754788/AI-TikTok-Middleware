"""
وحدة تحويل النص إلى صوت
Text to Speech Module
استخدام ElevenLabs لإنشاء صوت احترافي
"""
import requests
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, AUDIO_OUTPUT_DIR
import os
from datetime import datetime


class TextToSpeech:
    """فئة تحويل النص إلى صوت"""

    def __init__(self):
        self.api_key = ELEVENLABS_API_KEY
        self.voice_id = ELEVENLABS_VOICE_ID
        self.base_url = "https://api.elevenlabs.io/v1"

    def generate_audio(self, text: str, output_filename: str = None) -> str:
        """
        تحويل النص إلى صوت
        Convert text to speech using ElevenLabs
        
        Args:
            text: النص المراد تحويله
            output_filename: اسم الملف الناتج (اختياري)
        
        Returns:
            مسار الملف الصوتي
        """
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not configured")

        # إنشاء اسم الملف تلقائياً إذا لم يتم تحديده
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"audio_{timestamp}.mp3"

        output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)

        # ElevenLabs API endpoint
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"

        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            # حفظ الملف الصوتي
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"✅ تم إنشاء الملف الصوتي: {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ في إنشاء الملف الصوتي: {e}")
            raise

    def get_available_voices(self) -> list:
        """
        الحصول على قائمة الأصوات المتاحة
        Get list of available voices
        """
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not configured")

        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["voices"]
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ في الحصول على الأصوات: {e}")
            return []


# مثال على الاستخدام
if __name__ == "__main__":
    tts = TextToSpeech()

    # نص تجريبي
    test_text = "مرحبا! هذا مثال على تحويل النص إلى صوت باستخدام ElevenLabs"

    print("🎤 تحويل النص إلى صوت...")
    audio_file = tts.generate_audio(test_text, "test_audio.mp3")
    print(f"📁 تم حفظ الملف في: {audio_file}")
