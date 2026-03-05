import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")

    RATES_TTL_SECONDS = 7200  # 2 часа

    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN not found in .env")
