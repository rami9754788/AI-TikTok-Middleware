"""
ملف الإعدادات الرئيسي
Configuration file for AI TikTok Middleware
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"

# ElevenLabs Configuration (Text to Speech)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

# TikTok Configuration
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")

# Google Cloud Configuration (اختياري)
GOOGLE_CLOUD_KEY = os.getenv("GOOGLE_CLOUD_KEY")

# Telegram Bot (للإشعارات)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# General Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
MAX_VIDEOS_PER_DAY = int(os.getenv("MAX_VIDEOS_PER_DAY", 3))
VIDEO_DURATION = int(os.getenv("VIDEO_DURATION", 60))  # بالثواني
VIDEO_OUTPUT_DIR = "generated_videos"
AUDIO_OUTPUT_DIR = "generated_audio"

# Create directories if they don't exist
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
