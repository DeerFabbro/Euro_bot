import base64
import json
from google import genai
from google.genai import types
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

LANGUAGE_NAMES = {
    "RU": "русский",
    "EN": "английский",
    "IT": "итальянский"
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


def build_info_prompt(product: str, language: str = "RU") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "русский")
    return f"""
Найди краткую информацию о товаре: {product}

Ответь на {lang_name} языке в 3-4 предложениях. Включи:
- производитель и страна
- основные характеристики или состав
- для чего используется
- общая репутация или отзывы если известны

Только текст, без заголовков и списков.
"""


def build_price_evaluation_prompt(product: str, price: float, currency: str, language: str = "RU") -> str:
    lang_name = LANGUAGE_NAMES.get(language, "русский")
    return f"""
Оцени цену товара: {product}
Цена: {price} {currency}

По валюте {currency} и названию товара определи страну и типичный рынок.
Ответь на {lang_name} языке в 1-2 предложениях.
Скажи дорого это, нормально или дёшево для данной страны и рынка.
Если уместно — дай краткий совет (например, где найти дешевле).
Только текст, без заголовков.
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


async def get_price_evaluation(product: str, price: float, currency: str, language: str = "RU") -> str:
    import logging
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_price_evaluation_prompt(product, price, currency, language),
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        logging.info(f"PRICE EVAL RESPONSE: {repr(response.text)}")
        return response.text.strip() if response.text else None
    except Exception as e:
        logging.error(f"PRICE EVAL ERROR: {repr(e)}")
        return None


async def get_product_info(product: str, language: str = "RU") -> str:
    import logging
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_info_prompt(product, language),
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        logging.info(f"PRODUCT INFO RESPONSE: {repr(response.text)}")
        return response.text.strip() if response.text else None
    except Exception as e:
        logging.error(f"GET_PRODUCT_INFO ERROR: {repr(e)}")
        return None