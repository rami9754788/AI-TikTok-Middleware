"""
الملف الرئيسي للوسيط
Main Application File
ربط جميع الوحدات معاً في تطبيق واحد
"""
import schedule
import time
from datetime import datetime
from content_generator import ContentGenerator
from text_to_speech import TextToSpeech
from video_creator import VideoCreator
from tiktok_poster import TikTokPoster
from config import MAX_VIDEOS_PER_DAY, DEBUG
import logging

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ai_tiktok.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AITikTokMiddleware:
    """فئة الوسيط الرئيسية"""

    def __init__(self):
        self.content_generator = ContentGenerator()
        self.tts = TextToSpeech()
        self.video_creator = VideoCreator()
        self.tiktok_poster = TikTokPoster()
        self.videos_created_today = 0

    def generate_content(self, topic: str = None) -> dict:
        """
        توليد محتوى جديد
        Generate new content
        """
        logger.info("🎬 جاري توليد محتوى جديد...")
        
        try:
            # توليد فكرة
            idea = self.content_generator.generate_video_idea(topic)
            logger.info(f"💡 الفكرة: {idea}")

            # توليد السيناريو
            script = self.content_generator.generate_video_script(idea)
            logger.info(f"📝 السيناريو تم إنشاؤه")

            # دمج النص الكامل
            full_text = f"{script.get('intro', '')} {script.get('main_content', '')} {script.get('outro', '')}"

            return {
                "idea": idea,
                "script": script,
                "full_text": full_text,
                "hashtags": script.get("hashtags", ""),
                "status": "success"
            }

        except Exception as e:
            logger.error(f"❌ خطأ في توليد المحتوى: {e}")
            return {"status": "error", "message": str(e)}

    def create_video(self, content: dict) -> str:
        """
        إنشاء فيديو من المحتوى
        Create video from content
        """
        logger.info("🎥 جاري إنشاء الفيديو...")

        try:
            # تحويل النص إلى صوت
            logger.info("🎤 جاري تحويل النص إلى صوت...")
            audio_file = self.tts.generate_audio(
                content["full_text"],
                output_filename=f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            )

            # تحميل صورة خلفية
            logger.info("🖼️ جاري تحميل صورة خلفية...")
            bg_image = self.video_creator.download_background_image(
                content["idea"][:50]  # استخدام جزء من الفكرة كعنوان البحث
            )

            # إنشاء الفيديو
            logger.info("🎬 جاري دمج الصوت والصورة...")
            video_file = self.video_creator.create_video_with_text_overlay(
                audio_path=audio_file,
                text=content["script"].get("intro", ""),
                image_path=bg_image,
                output_filename=f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            )

            logger.info(f"✅ تم إنشاء الفيديو: {video_file}")
            return video_file

        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء الفيديو: {e}")
            return None

    def post_to_tiktok(self, video_file: str, content: dict) -> bool:
        """
        نشر الفيديو على TikTok
        Post video to TikTok
        """
        logger.info("📤 جاري النشر على TikTok...")

        try:
            # تحضير النص مع الهاشتاجات
            caption = f"{content['script'].get('intro', '')}\n{content.get('hashtags', '')}"

            # تهيئة المتصفح
            if not self.tiktok_poster.initialize_driver():
                logger.error("❌ فشل تهيئة المتصفح")
                return False

            # تسجيل الدخول
            if not self.tiktok_poster.login():
                logger.error("❌ فشل تسجيل الدخول")
                self.tiktok_poster.close()
                return False

            # رفع الفيديو
            success = self.tiktok_poster.upload_video(video_file, caption)

            # إغلاق المتصفح
            self.tiktok_poster.close()

            if success:
                logger.info("✅ تم النشر على TikTok بنجاح!")
                self.videos_created_today += 1

            return success

        except Exception as e:
            logger.error(f"❌ خطأ في النشر: {e}")
            return False

    def create_and_post_video(self, topic: str = None):
        """
        إنشاء ونشر فيديو كامل
        Create and post complete video
        """
        logger.info("=" * 50)
        logger.info(f"🚀 بدء إنشاء ونشر فيديو جديد - {datetime.now()}")
        logger.info("=" * 50)

        # التحقق من الحد الأقصى للفيديوهات اليومية
        if self.videos_created_today >= MAX_VIDEOS_PER_DAY:
            logger.warning(f"⚠️ تم الوصول للحد الأقصى ({MAX_VIDEOS_PER_DAY}) من الفيديوهات اليوم")
            return

        # توليد المحتوى
        content = self.generate_content(topic)
        if content.get("status") != "success":
            logger.error("❌ فشل توليد المحتوى")
            return

        # إنشاء الفيديو
        video_file = self.create_video(content)
        if not video_file:
            logger.error("❌ فشل إنشاء الفيديو")
            return

        # نشر على TikTok
        if not DEBUG:  # في وضع التطوير، لا ننشر فعلاً
            self.post_to_tiktok(video_file, content)
        else:
            logger.info("🧪 وضع التطوير - لم يتم النشر الفعلي")

        logger.info("=" * 50)
        logger.info(f"✅ انتهى إنشاء الفيديو - {datetime.now()}")
        logger.info("=" * 50)

    def schedule_daily_posts(self, time_str: str = "12:00"):
        """
        جدولة النشر اليومي
        Schedule daily posts
        
        Args:
            time_str: الوقت بصيغة HH:MM
        """
        schedule.every().day.at(time_str).do(self.create_and_post_video)
        logger.info(f"📅 تم جدولة النشر اليومي في الساعة {time_str}")

    def run_scheduler(self):
        """
        تشغيل جدول المهام
        Run the scheduler
        """
        logger.info("🔄 بدء مراقب الجدول...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # التحقق كل دقيقة

    def run_once(self, topic: str = None):
        """
        تشغيل لمرة واحدة
        Run once
        """
        self.create_and_post_video(topic)


# الدالة الرئيسية
def main():
    """
    نقطة البداية للتطبيق
    Application entry point
    """
    logger.info("🤖 بدء تطبيق AI TikTok Middleware")
    logger.info(f"وضع التطوير: {DEBUG}")

    middleware = AITikTokMiddleware()

    # خيارات التشغيل
    print("\n" + "=" * 50)
    print("🤖 AI TikTok Middleware")
    print("=" * 50)
    print("1️⃣ إنشاء ونشر فيديو واحد")
    print("2️⃣ جدولة النشر اليومي")
    print("3️⃣ الخروج")
    print("=" * 50)

    choice = input("اختر خياراً: ").strip()

    if choice == "1":
        topic = input("أدخل الموضوع (اتركه فارغاً للاختيار العشوائي): ").strip()
        middleware.run_once(topic if topic else None)

    elif choice == "2":
        time_input = input("أدخل وقت النشر (HH:MM) [الافتراضي: 12:00]: ").strip()
        time_to_post = time_input if time_input else "12:00"
        middleware.schedule_daily_posts(time_to_post)
        middleware.run_scheduler()

    elif choice == "3":
        logger.info("👋 الخروج من التطبيق")
        exit(0)

    else:
        print("❌ اختيار غير صحيح")


if __name__ == "__main__":
    main()
