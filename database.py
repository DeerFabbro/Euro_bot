import aiosqlite
from datetime import datetime

DB_PATH = "bot.db"
db = None


async def init_db():
    global db
    db = await aiosqlite.connect(DB_PATH)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            home_currency TEXT,
            language TEXT,
            created_at TEXT
        )
    """)

    await db.commit()


async def create_user_if_not_exists(user_id: int):
    async with db.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        user = await cursor.fetchone()

    if not user:
        await db.execute(
            "INSERT INTO users (user_id, created_at) VALUES (?, ?)",
            (user_id, datetime.utcnow().isoformat())
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
