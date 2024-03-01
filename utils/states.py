from aiogram.filters.state import StatesGroup, State


class BookingState(StatesGroup):
    content = State()
    content_type = State()
    number_of_questions = State()
    number_by_person = State()
