from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


CURRENCIES = [
    "BYN", "CZK", "PLN",
    "EUR", "USD", "GBP",
    "HUF", "CHF", "RON",
    "SEK", "NOK", "DKK",
    "RUB"
]


def currency_keyboard(home_currency):

    currencies = [c for c in CURRENCIES if c != home_currency]

    buttons = []

    for currency in currencies:
        buttons.append(
            InlineKeyboardButton(
                text=currency,
                callback_data=f"currency:{currency}"
            )
        )

    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]

    return InlineKeyboardMarkup(inline_keyboard=rows)


def reverse_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Reverse",
                    callback_data="reverse"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main_menu"
                )
            ]
        ]
    )


def settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💱 Сменить валюту",
                    callback_data="settings_currency"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Сменить язык",
                    callback_data="settings_language"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main_menu"
                )
            ]
        ]
    )


def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💱 Конвертация",
                    callback_data="menu_convert"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Настройки",
                    callback_data="menu_settings"
                )
            ]
        ]
    )