from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

yes_or_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, зарегистрировать бронь")],
        [KeyboardButton(text="Нет, сбросить форму")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Вы говорите боту, мол, '
)

next_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пропустить")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Вы говорите боту, мол, '
)

garik_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меня зовут Гарик"),
        ],
        [
            KeyboardButton(text="Нет")
        ],
        [
            KeyboardButton(text="Что?")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Играете на камнях?'
)

