from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from utils.states import *
from keyboards.keyboards import *
from model_db import *
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(FormState.about_player)
async def form_state_about_player(message: Message, state: FSMContext):
    data: str
    is_text: bool

    await message.answer(f"Интересно... Так и запишем...")
    await state.update_data(about_player=data)

    state_data = await state.get_data()

    await state.set_state(FormState.what_to_do)
    await message.answer(f"Чем бы Вы хотели заниматься на сервере? Есть ли у Вас какая-то цель?\n"
                         f"<i>Вам необходимо дать развернутый ответ. \n"
                         f"\n"
                         f"Вы можете отправить голосовое сообщение или текст</i>\n"
                         f"<b>Вопрос 2/4</b>")

