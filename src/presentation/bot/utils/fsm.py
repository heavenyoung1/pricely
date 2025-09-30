from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.fsm import StatesGroup

class ProductAddState(StatesGroup):
    waiting_for_url = State()  # Ожидаем URL товара