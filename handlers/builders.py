from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_keyboard(booking_id, topics_ids, busies=[]):
    builder_keyboard = InlineKeyboardBuilder()

    for i, j in topics_ids.items():
        if i in busies:
            j = f'✅{j}'
        builder_keyboard.button(text=f"{j}", callback_data=f"{booking_id},{i}")

    return builder_keyboard.as_markup()

