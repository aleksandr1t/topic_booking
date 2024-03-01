from aiogram.types import CallbackQuery
from model_db import *


async def select_verdict(call: CallbackQuery):
    form_id = int(call.data.split(',')[0])
    verdict = int(call.data.split(',')[1])

    await call.answer()


