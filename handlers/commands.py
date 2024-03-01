from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from utils import states
from datetime import datetime
from model_db import *

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    pass


@router.message(Command('make_booking'))
async def command_make_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(states.BookingState.content)
    await message.answer(f"Отправьте темы для выбора\n\n"
                         f""
                         f"<i>Вы можете отправить картинку (картинки) или текст."
                         f"Текст на картинке распознан не будет, людям будет предложено просто выбрать номер темы."
                         f"Если вы решите отправить текст, "
                         f"каждый вопрос должен отделяться переносом строки для распозновния вопросов. Например,</i>"
                         f"<b>1. Вопрос 1"
                         f"2. Вопрос 2...</b>")
