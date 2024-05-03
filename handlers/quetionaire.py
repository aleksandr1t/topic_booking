import datetime

from aiogram import Router
from aiogram.types import ReplyKeyboardRemove
from utils.states import *
from keyboards.keyboards import *
from model_db import *
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Create.photos_ids)
async def create_photos_ids(message: Message, state: FSMContext):
    if message.text:
        if message.text.lower() == 'дальше':
            data = await state.get_data()

            was_photos = False
            for key in data.keys():
                if key == 'photos_ids':
                    was_photos = True
            if not was_photos:
                await message.answer(f"Ты не отправил ни единого фото!")
                return
            else:
                await state.set_state(Create.quantity_of_topics)
                await message.answer(f"Напишите, какое количество тем будет.\n"
                                     f"\n"
                                     f"<i>Обычно это 30 </i>🤨\n"
                                     f"<b>Вопрос 2/3</b>", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f"🙄")
            return
    if not message.photo and not message.text:
        await message.answer(f"Так дело не идет, фотографии отправляй")
        return
    else:
        data = await state.get_data()

        was_photos = False
        for key in data.keys():
            if key == 'photos_ids':
                was_photos = True

        await message.bot.download(file=message.photo[-1].file_id, destination=f'photos/{message.photo[-1].file_id}.jpg')
        if was_photos:
            photos_ids = data['photos_ids']
            photos_ids.append(message.photo[-1].file_id)
        else:
            photos_ids = [message.photo[-1].file_id]
        await state.update_data(photos_ids=photos_ids)


@router.message(Create.quantity_of_topics)
async def select_quantity_of_topics(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(f"Скинь цифоркой на клавиатуре количество тем пожалуйсто🥺")
        return
    else:
        try:
            quantity = int(message.text)
        except ValueError:
            await message.answer(f"Скинь цифоркой на клавиатуре количество тем пожалуйстаааааааааа🤠")
            return
        await message.answer(f"Так-с...")

    await message.answer(f"Записал. Идем дальше")
    await state.update_data(quantity_of_topics=quantity)
    await state.set_state(Create.people_for_topic)

    await message.answer(f"Напишите, какое количество людей может занимать одну тему.\n"
                         f"\n"
                         f"<i>Обычно это 1 </i>🤨\n"
                         f"<b>Вопрос 3/3</b>")


@router.message(Create.people_for_topic)
async def select_people_for_topic(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(f"Скинь текстом пожалуйсто😢")
        return
    else:
        try:
            people_for_topic = int(message.text)
        except ValueError:
            await message.answer(f"Скинь цифоркой пожалуйстаааааааааа😧")
            return
        await message.answer(f"Значит-ся, все записали.")

    await state.update_data(people_for_topic=people_for_topic)
    await state.set_state(Create.okay_bro_yeah_mazafaka)
    await message.answer(f"Вы уверены, что хотите \"открыть бронь\"?", reply_markup=yes_or_no_keyboard)


@router.message(Create.okay_bro_yeah_mazafaka)
async def confidence(message: Message, state: FSMContext):
    if message.text.lower() == 'да, зарегистрировать бронь':
        data = await state.get_data()

        with db:
            booking = Booking.create(time_of_creation=datetime.datetime.now(), telegram_id=message.from_user.id,
                                     times_can_choose=data['people_for_topic'])
            for photo_id in data['photos_ids']:
                Photos.create(photo_id=photo_id, booking_id=booking.id)
            for topic in range(data['quantity_of_topics']):
                TopicList.create(time_of_creation=datetime.datetime.now(),
                                 booking_id=booking.id, topic_in_booking_id=topic+1)
        await message.answer('Создано!', reply_markup=ReplyKeyboardRemove())

        # отправляется сообщение

    elif message.text.lower() == 'нет, сбросить форму':
        await message.answer('Ну и иди нахуй тогда', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('😐')
    await state.clear()
