"""
وحدة إنشاء الفيديوهات
Video Creation Module
دمج الصور والصوت والنصوص لإنشاء فيديو TikTok
"""
import os
from datetime import datetime
from config import VIDEO_OUTPUT_DIR, VIDEO_DURATION


class VideoCreator:
    """فئة إنشاء الفيديوهات"""

    def __init__(self):
        self.output_dir = VIDEO_OUTPUT_DIR
        self.video_duration = VIDEO_DURATION

    def create_video_from_audio_and_image(
        self, audio_path: str, image_path: str = None, output_filename: str = None
    ) -> str:
        """
        إنشاء فيديو من ملف صوتي وصورة
        Create video from audio file and image
        """
        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        except ImportError:
            print("❌ يجب تثبيت moviepy: pip install moviepy")
            return None

        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_{timestamp}.mp4"

        output_path = os.path.join(self.output_dir, output_filename)

        try:
            # تحميل الصوت
            audio = AudioFileClip(audio_path)
            audio_duration = audio.duration

            if image_path and os.path.exists(image_path):
                # إنشاء فيديو من صورة والصوت
                image = ImageClip(image_path)
                video = image.set_duration(audio_duration)
                video = video.set_audio(audio)
            else:
                print("⚠️ لم يتم العثور على الصورة، سيتم إنشاء فيديو بدون صور")
                return None

            # حفظ الفيديو
            video.write_videofile(
                output_path, fps=24, verbose=False, logger=None, audio_codec="aac"
            )

            print(f"✅ تم إنشاء الفيديو: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ خطأ في إنشاء الفيديو: {e}")
            return None

    def create_video_with_text_overlay(
        self,
        audio_path: str,
        text: str,
        image_path: str = None,
        output_filename: str = None,
    ) -> str:
        """
        إنشاء فيديو مع نصوص معروضة
        Create video with text overlay
        """
        try:
            from moviepy.editor import (
                ImageClip,
                AudioFileClip,
                TextClip,
                CompositeVideoClip,
            )
        except ImportError:
            print("❌ يجب تثبيت moviepy: pip install moviepy")
            return None

        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"video_text_{timestamp}.mp4"

        output_path = os.path.join(self.output_dir, output_filename)

        try:
            # تحميل الصوت
            audio = AudioFileClip(audio_path)
            audio_duration = audio.duration

            if image_path and os.path.exists(image_path):
                # إنشاء الفيديو من الصورة
                image = ImageClip(image_path)
                video = image.set_duration(audio_duration)

                # إضافة النص
                txt_clip = TextClip(
                    text,
                    fontsize=40,
                    color="white",
                    font="Arial-Bold",
                    method="caption",
                    size=(1080, 1920),
                )
                txt_clip = txt_clip.set_duration(audio_duration)
                txt_clip = txt_clip.set_position("center")

                # دمج الفيديو والنص والصوت
                video = CompositeVideoClip([video, txt_clip.set_opacity(0.9)])
                video = video.set_audio(audio)
            else:
                print("⚠️ لم يتم العثور على الصورة")
                return None

            # حفظ الفيديو
            video.write_videofile(
                output_path, fps=24, verbose=False, logger=None, audio_codec="aac"
            )

            print(f"✅ تم إنشاء الفيديو مع النصوص: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ خطأ في إنشاء الفيديو: {e}")
            return None

    def download_background_image(self, query: str, output_path: str = None) -> str:
        """
        تحميل صورة خلفية من الإنترنت
        Download background image from internet
        """
        try:
            from bing_image_downloader import bing_image_downloader
        except ImportError:
            print("❌ يجب تثبيت bing-image-downloader")
            return None

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"bg_{timestamp}.jpg")

        try:
            bing_image_downloader.download(
                query,
                limit=1,
                output_dir="dataset",
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
            )
            print(f"✅ تم تحميل الصورة")
            return output_path
        except Exception as e:
            print(f"⚠️ خطأ في تحميل الصورة: {e}")
            return None


# مثال على الاستخدام
if __name__ == "__main__":
    creator = VideoCreator()
    print("🎬 وحدة إنشاء الفيديوهات جاهزة")
