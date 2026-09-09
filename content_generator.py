"""
وحدة توليد المحتوى
Content Generation Module
استخدام OpenAI لإنشاء أفكار ونصوص المحتوى
"""
import openai
from config import OPENAI_API_KEY, OPENAI_MODEL
from typing import List, Dict

openai.api_key = OPENAI_API_KEY


class ContentGenerator:
    """فئة توليد المحتوى"""

    def __init__(self):
        self.model = OPENAI_MODEL

    def generate_video_idea(self, topic: str = None) -> str:
        """
        توليد فكرة فيديو جديدة
        Generate a new video idea
        """
        if topic is None:
            topic = "محتوى فيروسي مشهور"

        prompt = f"""
        أنا مشهور على TikTok أريد فكرة فيديو جديدة وفريدة وفيروسية عن: {topic}
        الفيديو يجب أن يكون:
        - مثير للاهتمام
        - قصير (60 ثانية)
        - سهل التنفيذ بالذكاء الاصطناعي
        - فيروسي وممل للمشاهدين
        
        أعطني فكرة واحدة فقط مختصرة
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=200,
        )

        return response.choices[0].message.content

    def generate_video_script(self, idea: str) -> Dict[str, str]:
        """
        توليد نص الفيديو والسيناريو
        Generate video script and narration
        """
        prompt = f"""
        اكتب نص قصير لفيديو TikTok (حوالي 60 ثانية) بناءً على هذه الفكرة:
        {idea}
        
        النص يجب أن يكون:
        1. جذاب منذ البداية
        2. مختصر وسريع
        3. يحتوي على عبارات قوية
        4. مناسب للنطق بصوت طبيعي
        
        أعطني النتيجة بصيغة JSON:
        {{
            "intro": "مقدمة جذابة",
            "main_content": "المحتوى الرئيسي",
            "outro": "خاتمة قوية",
            "hashtags": "الهاشتاجات المناسبة"
        }}
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )

        content = response.choices[0].message.content

        # محاولة استخراج JSON من الرد
        try:
            import json

            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
        except:
            pass

        return {
            "intro": "",
            "main_content": content,
            "outro": "",
            "hashtags": "#foryou #viral #foryoupage",
        }

    def generate_trending_topics(self) -> List[str]:
        """
        الحصول على المواضيع التريندينج الحالية
        Get current trending topics
        """
        prompt = """
        أعطني أفضل 5 مواضيع تريندينج على TikTok الآن التي يمكن إنشاء فيديوهات عنها
        اجعلها مختصرة وواضحة
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=300,
        )

        content = response.choices[0].message.content
        topics = [line.strip() for line in content.split("\n") if line.strip()]
        return topics[:5]


# مثال على الاستخدام
if __name__ == "__main__":
    generator = ContentGenerator()

    print("🎬 توليد فكرة فيديو...")
    idea = generator.generate_video_idea("كوميديا")
    print(f"الفكرة: {idea}\n")

    print("📝 توليد السيناريو...")
    script = generator.generate_video_script(idea)
    print(f"السيناريو: {script}\n")

    print("🔥 المواضيع التريندينج...")
    topics = generator.generate_trending_topics()
    for topic in topics:
        print(f"  - {topic}")
