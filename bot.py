import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

from config import Config
from database import (
    init_db,
    create_user_if_not_exists,
    get_user_settings,
    update_home_currency,
    update_language,
    get_selected_currencies,
    update_selected_currencies
)

from keyboards import (
    currency_keyboard,
    reverse_keyboard,
    settings_keyboard,
    main_menu_keyboard,
    my_currencies_keyboard,
    hint_keyboard
)

from services import convert
from vision import analyze_price_tag, get_product_details
import logging
logging.basicConfig(level=logging.INFO)

ONBOARDING_TEXT = """👋 Привет! Я Euro Smart Bot.

Умею:
💱 Конвертировать валюты — просто введи сумму
📷 Сканировать ценники — отправь фото и я переведу цену и расскажу о товаре
⚙️ Настройки — выбери домашнюю валюту, язык и список валют для конвертации"""


async def show_main_menu(message: Message):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu_keyboard()
    )


async def start_handler(message: Message):
    await create_user_if_not_exists(message.from_user.id)
    await message.answer(ONBOARDING_TEXT)
    await show_main_menu(message)


async def settings_handler(message: Message):
    settings = await get_user_settings(message.from_user.id)
    home_currency = settings[0]
    language = settings[1]
    text = (
        "⚙️ Настройки\n"
        f"Домашняя валюта: {home_currency}\n"
        f"Язык: {language}"
    )
    await message.answer(text, reply_markup=settings_keyboard())


async def menu_convert(callback: CallbackQuery):
    await callback.message.answer("Введите сумму для конвертации")
    await callback.answer()


async def menu_scan(callback: CallbackQuery):
    await callback.message.answer("📷 Отправьте фото ценника")
    await callback.answer()


async def menu_settings(callback: CallbackQuery):
    settings = await get_user_settings(callback.from_user.id)
    home_currency = settings[0]
    language = settings[1]
    text = (
        "⚙️ Настройки\n"
        f"Домашняя валюта: {home_currency}\n"
        f"Язык: {language}"
    )
    await callback.message.answer(text, reply_markup=settings_keyboard())
    await callback.answer()


async def main_menu(callback: CallbackQuery):
    await callback.message.answer(
        "👋 Я Euro Smart Bot.\nНе нужно искать кнопки — просто введи сумму или отправь фото ценника в любой момент. Я переведу цену, расскажу о товаре и оценю выгоду покупки.",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


async def settings_currency(callback: CallbackQuery):
    buttons = []
    for currency in [
        "BYN", "CZK", "PLN",
        "EUR", "USD", "GBP",
        "HUF", "CHF", "RON",
        "SEK", "NOK", "DKK",
        "RUB"
    ]:
        buttons.append(
            InlineKeyboardButton(
                text=currency,
                callback_data=f"setcurrency:{currency}"
            )
        )
    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
    await callback.message.answer("Выберите новую домашнюю валюту:", reply_markup=keyboard)
    await callback.answer()


async def set_currency(callback: CallbackQuery):
    currency = callback.data.split(":")[1]
    await update_home_currency(callback.from_user.id, currency)
    await callback.message.answer(
        f"Домашняя валюта обновлена: {currency}",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


async def settings_language(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="RU", callback_data="lang:RU"),
                InlineKeyboardButton(text="EN", callback_data="lang:EN"),
                InlineKeyboardButton(text="IT", callback_data="lang:IT"),
            ],
            [
                InlineKeyboardButton(text="DE", callback_data="lang:DE"),
                InlineKeyboardButton(text="FI", callback_data="lang:FI"),
                InlineKeyboardButton(text="PL", callback_data="lang:PL"),
            ],
            [
                InlineKeyboardButton(text="CS", callback_data="lang:CS"),
                InlineKeyboardButton(text="NL", callback_data="lang:NL"),
                InlineKeyboardButton(text="ES", callback_data="lang:ES"),
            ]
        ]
    )
    await callback.message.answer("Выберите язык:", reply_markup=keyboard)
    await callback.answer()


async def language_callback(callback: CallbackQuery):
    language = callback.data.split(":")[1]
    await update_language(callback.from_user.id, language)
    await callback.message.answer(
        f"Язык обновлён: {language}",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


async def settings_my_currencies(callback: CallbackQuery):
    selected = await get_selected_currencies(callback.from_user.id)
    await callback.message.answer(
        "☑️ Выберите валюты для конвертации:",
        reply_markup=my_currencies_keyboard(selected)
    )
    await callback.answer()


async def toggle_currency(callback: CallbackQuery):
    currency = callback.data.split(":")[1]
    selected = await get_selected_currencies(callback.from_user.id)

    if currency in selected:
        if len(selected) > 1:
            selected.remove(currency)
    else:
        selected.append(currency)

    await update_selected_currencies(callback.from_user.id, selected)

    await callback.message.edit_reply_markup(
        reply_markup=my_currencies_keyboard(selected)
    )
    await callback.answer()


async def save_currencies(callback: CallbackQuery):
    await callback.message.answer(
        "✅ Валюты сохранены",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


async def amount_handler(message: Message, state: FSMContext):
    if not message.text:
        return
    text = message.text.strip()
    try:
        amount = float(text.replace(",", "."))
    except ValueError:
        await message.answer(
            "Введите сумму для конвертации или отправьте фото ценника",
            reply_markup=hint_keyboard()
        )
        return
    await state.update_data(amount=amount)
    settings = await get_user_settings(message.from_user.id)
    home_currency = settings[0]
    selected = await get_selected_currencies(message.from_user.id)
    await message.answer(
        f"Сумма: {amount}\nВыберите валюту:",
        reply_markup=currency_keyboard(home_currency, selected)
    )


async def currency_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "amount" not in data:
        await callback.answer("Сначала введите сумму")
        return
    amount = data["amount"]
    currency = callback.data.split(":")[1]
    settings = await get_user_settings(callback.from_user.id)
    home_currency = settings[0]
    result = await convert(amount, currency, home_currency)
    await state.update_data(currency=currency)
    rate = round(result / amount, 4)
    await callback.message.answer(
        f"{amount} {currency} = {result} {home_currency}\n💱 1 {currency} = {rate} {home_currency}",
        reply_markup=reverse_keyboard()
    )
    await callback.answer()


async def reverse_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "amount" not in data or "currency" not in data:
        await callback.answer("Введите сумму заново")
        return
    amount = data["amount"]
    currency = data["currency"]
    settings = await get_user_settings(callback.from_user.id)
    home_currency = settings[0]
    result = await convert(amount, home_currency, currency)
    rate = round(result / amount, 4)
    await callback.message.answer(
        f"{amount} {home_currency} = {result} {currency} · 1 {home_currency} = {rate} {currency}",
        reply_markup=reverse_keyboard()
    )
    await callback.answer()


async def photo_handler(message: Message):
    logging.info("PHOTO RECEIVED")
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.answer("📷 Анализирую ценник...")

    settings = await get_user_settings(message.from_user.id)
    home_currency = settings[0]
    language = settings[1] or "RU"

    bot = message.bot
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    image_bytes = await bot.download_file(file.file_path)
    image_bytes = image_bytes.read()

    try:
        data = await analyze_price_tag(image_bytes, language)
    except Exception as e:
        logging.error(f"ANALYZE ERROR: {repr(e)}")
        await message.answer(
            "❌ Не удалось распознать ценник. Отправьте фото ценника или введите сумму для конвертации.",
            reply_markup=hint_keyboard()
        )
        return

    product = data.get("product") or "—"
    price = data.get("price")
    price_per_kg = data.get("price_per_kg")
    currency = data.get("currency")
    promo = data.get("promo")

    if not price or not currency:
        await message.answer(
            "❌ Это не похоже на ценник. Отправьте фото ценника или введите сумму для конвертации.",
            reply_markup=hint_keyboard()
        )
        return

    try:
        converted = await convert(float(price), currency, home_currency)
    except Exception:
        converted = None

    lines = [f"🛒 {product}"]
    lines.append(f"💶 {price} {currency}")

    if converted:
        lines.append(f"💵 {converted} {home_currency}")

    if price_per_kg:
        try:
            converted_kg = await convert(float(price_per_kg), currency, home_currency)
            lines.append(f"📦 За кг: {price_per_kg} {currency} → {converted_kg} {home_currency}")
        except Exception:
            lines.append(f"📦 За кг: {price_per_kg} {currency}")

    if promo:
        lines.append(f"🏷 {promo}")

    # Сообщение 1 — результат скана
    await message.answer("\n".join(lines))

    # Сообщения 2 и 3 — один запрос к Gemini
    if product and product != "—" and price:
        info, evaluation = await get_product_details(
            product, float(price), currency, language,
            float(price_per_kg) if price_per_kg else None,
            float(data.get("weight")) if data.get("weight") else None
        )
        if evaluation:
            await message.answer(f"💰 {evaluation}")
        if info:
            await message.answer(f"ℹ️ {info}", reply_markup=hint_keyboard())
            return

    await message.answer("🏠", reply_markup=hint_keyboard())


async def main():
    Config.validate()
    await init_db()

    bot = Bot(token=Config.TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.register(start_handler, CommandStart())
    dp.message.register(settings_handler, Command("settings"))
    dp.message.register(photo_handler, F.photo)
    dp.message.register(amount_handler)

    dp.callback_query.register(menu_convert, F.data == "menu_convert")
    dp.callback_query.register(menu_scan, F.data == "menu_scan")
    dp.callback_query.register(menu_settings, F.data == "menu_settings")
    dp.callback_query.register(main_menu, F.data == "main_menu")
    dp.callback_query.register(settings_currency, F.data == "settings_currency")
    dp.callback_query.register(set_currency, F.data.startswith("setcurrency:"))
    dp.callback_query.register(settings_language, F.data == "settings_language")
    dp.callback_query.register(language_callback, F.data.startswith("lang:"))
    dp.callback_query.register(settings_my_currencies, F.data == "settings_my_currencies")
    dp.callback_query.register(toggle_currency, F.data.startswith("toggle_currency:"))
    dp.callback_query.register(save_currencies, F.data == "save_currencies")
    dp.callback_query.register(currency_callback, F.data.startswith("currency:"))
    dp.callback_query.register(reverse_callback, F.data == "reverse")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())