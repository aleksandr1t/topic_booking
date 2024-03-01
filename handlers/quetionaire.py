from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from utils.states import *
from keyboards.keyboards import *
from model_db import *
from aiogram.fsm.context import FSMContext
import os

router = Router()


@router.message(BookingState.content)
async def form_state_about_player(message: Message, state: FSMContext):
    topics = []
    if not message.text or not message.photo:
        await message.answer(f"ОТПРАВЬ ПОЖАЛУЙСТА ФОТО ИЛИ ТЕКСТ")
        return
    if message.text:
        content_type = 'text'
        topics = message.text.split('\n')
    else:
        content_type = 'photo'
        photos = message.photo
        for photo in photos:
            if not os.path.exists(f'files/{message.from_user.id}'):
                os.mkdir(f'files/{message.from_user.id}')
            topics.append(photo)
            await photo.download(f'files/{message.from_user.id}/{photo.file_id}.jpg')
    await state.update_data(content_type=content_type)
    await state.update_data(content=topics)

    state_data = await state.get_data()

    await state.set_state(FormState.what_to_do)
    await message.answer(f"")
