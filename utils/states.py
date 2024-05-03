from aiogram.filters.state import StatesGroup, State


class Create(StatesGroup):
    photos_ids = State()
    quantity_of_topics = State()
    people_for_topic = State()
    okay_bro_yeah_mazafaka = State()
    photo_fix = State()
