import aiohttp
import time
from config import Config

SUPPORTED_CURRENCIES = {
    "RUB", "EUR", "USD",
    "BYN", "PLN", "CZK", "HUF",
    "CHF", "GBP", "RSD",
    "RON", "SEK", "NOK", "DKK"
}

_rates_cache = None
_last_update = 0


async def get_rates(base: str = "EUR"):
    global _rates_cache, _last_update

    now = time.time()

    # Кэш 2 часа
    if _rates_cache and (now - _last_update < Config.RATES_TTL_SECONDS):
        return _rates_cache

    url = f"https://v6.exchangerate-api.com/v6/{Config.EXCHANGE_API_KEY}/latest/{base}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    if data.get("result") != "success":
        raise Exception("Ошибка получения курсов")

    _rates_cache = data["conversion_rates"]
    _last_update = now

    return _rates_cache


async def convert(amount: float, from_currency: str, to_currency: str):

    if from_currency not in SUPPORTED_CURRENCIES:
        raise ValueError("Валюта не поддерживается")

    if to_currency not in SUPPORTED_CURRENCIES:
        raise ValueError("Валюта не поддерживается")

    if from_currency == to_currency:
        return round(amount, 2)

    # Всегда берём курсы относительно EUR
    rates = await get_rates(base="EUR")

    from_rate = rates.get(from_currency)
    to_rate = rates.get(to_currency)

    if not from_rate or not to_rate:
        raise ValueError("Курс не найден")

    # конвертация через EUR
    result = amount / from_rate * to_rate

    return round(result, 2)