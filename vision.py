import base64
import json
from google import genai
from google.genai import types
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

PROMPT = """
Ты анализируешь фото ценника из магазина.
Извлеки данные и верни ТОЛЬКО валидный JSON без markdown, без пояснений.

Формат:
{
  "product": "название товара или null",
  "price": число или null,
  "price_per_kg": число или null,
  "currency": "код валюты ISO 4217 или null",
  "promo": "описание акции или null"
}

Если цена не найдена — верни price: null.
Валюту определяй по символу: € = EUR, $ = USD, £ = GBP, zł = PLN, Kč = CZK и т.д.
"""


async def analyze_price_tag(image_bytes: bytes) -> dict:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        inline_data=types.Blob(
                            mime_type="image/jpeg",
                            data=image_base64
                        )
                    ),
                    types.Part(text=PROMPT)
                ]
            )
        ]
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)
    return result
