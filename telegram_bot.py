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
from typing import Callable, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message
import asyncio
import logging
import sys
from aiogram.types import FSInputFile
from aiogram.fsm.storage.redis import RedisStorage


TOKEN = TOKEN_epta
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

# storage = RedisStorage(redis.Redis(host="172.31.99.45", port=6379, username="kposhnik", password=f'{rediska}'))

dp = Dispatcher()
dp.callback_query.register(callback.select_topic)


class SomeMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data['_is_last'] = True
            data["album"] = self.album_data[message.media_group_id]
            await handler(message, data)

        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data['_is_last']


async def main():
    dp.message.middleware(SomeMiddleware())
    dp.include_routers(quetionaire.router, commands.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
