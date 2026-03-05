from aiogram.fsm.state import State, StatesGroup


class Onboarding(StatesGroup):
    choosing_currency = State()
    choosing_language = State()
