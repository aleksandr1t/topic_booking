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


@router.message(Command('new_form'))
async def command_new_form(message: Message, state: FSMContext) -> None:
    pass
