import aiosqlite
import json
from datetime import datetime

DB_PATH = "bot.db"
db = None

DEFAULT_CURRENCIES = ["BYN", "CZK", "PLN", "EUR", "USD", "GBP", "HUF", "CHF", "RON", "SEK", "NOK", "DKK", "RUB"]


async def init_db():
    global db
    db = await aiosqlite.connect(DB_PATH)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            home_currency TEXT,
            language TEXT,
            created_at TEXT,
            selected_currencies TEXT
        )
    """)

    # Добавить колонку если её нет (для существующих БД)
    try:
        await db.execute("ALTER TABLE users ADD COLUMN selected_currencies TEXT")
        await db.commit()
    except Exception:
        pass

    await db.commit()


async def create_user_if_not_exists(user_id: int):
    async with db.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        user = await cursor.fetchone()

    if not user:
        await db.execute(
            "INSERT INTO users (user_id, created_at, selected_currencies) VALUES (?, ?, ?)",
            (user_id, datetime.utcnow().isoformat(), json.dumps(DEFAULT_CURRENCIES))
        )
        await db.commit()


async def update_home_currency(user_id: int, currency: str):
    await db.execute(
        "UPDATE users SET home_currency = ? WHERE user_id = ?",
        (currency, user_id)
    )
    await db.commit()


async def get_user_settings(user_id: int):
    async with db.execute(
        "SELECT home_currency, language FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        return await cursor.fetchone()


async def update_language(user_id: int, language: str):
    await db.execute(
        "UPDATE users SET language = ? WHERE user_id = ?",
        (language, user_id)
    )
    await db.commit()


async def get_selected_currencies(user_id: int):
    async with db.execute(
        "SELECT selected_currencies FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
    if row and row[0]:
        return json.loads(row[0])
    return DEFAULT_CURRENCIES


async def update_selected_currencies(user_id: int, currencies: list):
    await db.execute(
        "UPDATE users SET selected_currencies = ? WHERE user_id = ?",
        (json.dumps(currencies), user_id)
    )
    await db.commit()