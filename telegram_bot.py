import os
import redis.asyncio as redis
from model_db import *
from utils import states
from config import TOKEN_epta, rediska
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from handlers import quetionaire, builders
from aiogram.fsm.storage.base import StorageKey, BaseStorage
from handlers import commands
from handlers import callback
import asyncio
import logging
import sys
from aiogram.types import FSInputFile
from aiogram.fsm.storage.redis import RedisStorage


TOKEN = TOKEN_epta
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# storage = RedisStorage(redis.Redis(host="172.31.99.45", port=6379, username="kposhnik", password=f'{rediska}'))

dp = Dispatcher()
# dp.callback_query.register(callback.select_verdict)


async def main():
    dp.include_routers(quetionaire.router, commands.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
