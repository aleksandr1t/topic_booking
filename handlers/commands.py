import random

from aiogram import Router, F
from aiogram.types import Message, input_file
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import keyboards.keyboards
from utils import states
from datetime import datetime
from model_db import *
from config import trusted_ids

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Здраствуй, {message.from_user.first_name}\n")


@router.message(Command('new_booking'))
async def command_new_booking(message: Message, state: FSMContext) -> None:
    if message.from_user.id not in trusted_ids:
        await message.answer(f"Вас нет в списке доверенных лиц, "
                             f"позволяемым создание записи. Но не растраиваетесь! Держите котика!")
        cat_id = str(random.randint(1, 10))
        await message.bot.send_photo(message.chat.id, input_file.FSInputFile(f'cats/{cat_id}.jpg'))
        return

    await state.set_state(states.Create.photos_ids)
    await message.answer(f"Отправьте фотографии тем.\n"
                         f"\n"
                         f"<i>Вы можете отправить до 1488 фото. Как только закончите отправлять фотографии, "
                         f"нажмите на кнопку <b>Дальше</b></i>\n"
                         f"<b>Вопрос 1/4</b>")

