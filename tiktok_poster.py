"""
وحدة نشر المحتوى على TikTok
TikTok Posting Module
استخدام Selenium للنشر التلقائي
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import TIKTOK_USERNAME, TIKTOK_PASSWORD
import os


class TikTokPoster:
    """فئة نشر المحتوى على TikTok"""

    def __init__(self):
        self.username = TIKTOK_USERNAME
        self.password = TIKTOK_PASSWORD
        self.driver = None

    def initialize_driver(self):
        """
        تهيئة متصفح Selenium
        Initialize Selenium browser
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=options)
            print("✅ تم تهيئة المتصفح")
            return True
        except Exception as e:
            print(f"❌ خطأ في تهيئة المتصفح: {e}")
            return False

    def login(self) -> bool:
        """
        تسجيل الدخول إلى TikTok
        Login to TikTok
        """
        try:
            self.driver.get("https://www.tiktok.com/login")
            time.sleep(3)

            # انتظار حقل اسم المستخدم
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)

            # إدخال كلمة المرور
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)

            # الضغط على زر تسجيل الدخول
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # انتظار تحميل الصفحة الرئيسية
            time.sleep(5)
            print("✅ تم تسجيل الدخول بنجاح")
            return True

        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول: {e}")
            return False

    def upload_video(self, video_path: str, caption: str) -> bool:
        """
        رفع فيديو على TikTok
        Upload video to TikTok
        
        Args:
            video_path: مسار ملف الفيديو
            caption: نص الفيديو والهاشتاجات
        """
        try:
            if not os.path.exists(video_path):
                print(f"❌ الملف غير موجود: {video_path}")
                return False

            # الذهاب إلى صفحة تحميل الفيديو
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)

            # العثور على حقل رفع الملف
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )

            # رفع الملف
            file_input.send_keys(os.path.abspath(video_path))
            print(f"📤 جاري رفع الفيديو: {video_path}")

            # انتظار اكتمال الرفع
            time.sleep(10)

            # إضافة النص والهاشتاجات
            caption_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea"))
            )
            caption_input.send_keys(caption)

            print(f"📝 تمت إضافة النص: {caption}")

            # الضغط على زر النشر
            publish_button = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Post')]"
            )
            publish_button.click()

            # انتظار النشر
            time.sleep(10)
            print("✅ تم نشر الفيديو بنجاح!")
            return True

        except Exception as e:
            print(f"❌ خطأ في رفع الفيديو: {e}")
            return False

    def close(self):
        """إغلاق المتصفح"""
        if self.driver:
            self.driver.quit()
            print("🔌 تم إغلاق المتصفح")


# مثال على الاستخدام
if __name__ == "__main__":
    poster = TikTokPoster()

    if poster.initialize_driver():
        if poster.login():
            # رفع فيديو تجريبي
            video_file = "generated_videos/test_video.mp4"
            caption = "فيديو تجريبي من الذكاء الاصطناعي 🤖 #AI #TikTok #FYP"

            poster.upload_video(video_file, caption)

        poster.close()
