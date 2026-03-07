from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


CURRENCIES = [
    "BYN", "CZK", "PLN",
    "EUR", "USD", "GBP",
    "HUF", "CHF", "RON",
    "SEK", "NOK", "DKK",
    "RUB"
]


def currency_keyboard(home_currency, selected_currencies=None):
    if selected_currencies is None:
        selected_currencies = CURRENCIES

    currencies = [c for c in selected_currencies if c != home_currency]

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
                    text="☑️ Мои валюты",
                    callback_data="settings_my_currencies"
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


def my_currencies_keyboard(selected_currencies):
    buttons = []
    for currency in CURRENCIES:
        is_selected = currency in selected_currencies
        buttons.append(
            InlineKeyboardButton(
                text=f"✅ {currency}" if is_selected else f"◻️ {currency}",
                callback_data=f"toggle_currency:{currency}"
            )
        )

    rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]

    rows.append([
        InlineKeyboardButton(
            text="✔️ Сохранить",
            callback_data="save_currencies"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


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
                    text="📷 Сканировать ценник",
                    callback_data="menu_scan"
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