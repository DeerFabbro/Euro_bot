import base64
import json
from google import genai
from google.genai import types
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

LANGUAGE_NAMES = {
    "RU": "русский",
    "EN": "английский",
    "IT": "итальянский",
    "DE": "немецкий",
    "FI": "финский",
    "PL": "польский",
    "CS": "чешский",
    "NL": "нидерландский",
    "ES": "испанский"
}


def build_prompt(language: str = "RU") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "русский")
    return f"""
Ты анализируешь фото ценника из магазина.
Извлеки данные и верни ТОЛЬКО валидный JSON без markdown, без пояснений.

Формат:
{{
  "product": "название товара на {lang_name} языке или null",
  "price": число или null,
  "price_per_kg": число или null,
  "currency": "код валюты ISO 4217 или null",
  "promo": "описание акции или null"
}}

Если цена не найдена — верни price: null.
Валюту определяй по символу: € = EUR, $ = USD, £ = GBP, zł = PLN, Kč = CZK, руб = RUB и т.д.
Название товара переведи на {lang_name} язык.
"""


def build_combined_prompt(product: str, price: float, currency: str, language: str = "RU") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "русский")
    return f"""
Товар: {product}
Цена: {price} {currency}

Ответь на {lang_name} языке. Верни ТОЛЬКО два абзаца без заголовков:

Абзац 1 — краткая информация о товаре (3-4 предложения):
- производитель и страна
- основные характеристики или состав
- для чего используется
- общая репутация или отзывы

Абзац 2 — оценка цены (1-2 предложения):
По валюте {currency} и названию товара определи страну и рынок.
Если цена НИЗКАЯ: напиши что цена хорошая, и если качество не вызывает сомнений — стоит брать.
Если цена СРЕДНЯЯ: напиши что цена нормальная для данного рынка.
Если цена ВЫСОКАЯ: напиши что стоит поискать дешевле, и назови конкретные альтернативы — дискаунтеры или магазины данной категории товара в данной стране.

Разделяй абзацы пустой строкой. Только текст, без заголовков и списков.
"""


async def analyze_price_tag(image_bytes: bytes, language: str = "RU") -> dict:
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
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
                    types.Part(text=build_prompt(language))
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


async def get_product_details(product: str, price: float, currency: str, language: str = "RU") -> tuple[str, str]:
    import logging
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_combined_prompt(product, price, currency, language),
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        logging.info(f"PRODUCT DETAILS RESPONSE: {repr(response.text)}")
        text = response.text.strip() if response.text else None
        if not text:
            return None, None
        parts = text.split("\n\n", 1)
        info = parts[0].strip() if len(parts) > 0 else None
        evaluation = parts[1].strip() if len(parts) > 1 else None
        return info, evaluation
    except Exception as e:
        logging.error(f"PRODUCT DETAILS ERROR: {repr(e)}")
        return None, None