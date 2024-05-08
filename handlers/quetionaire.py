import asyncio
import datetime

from aiogram import Router
from aiogram.types import ReplyKeyboardRemove, input_file
from aiogram.utils import media_group
from utils.states import *
from handlers import builders
from keyboards.keyboards import *
from model_db import *
from aiogram.fsm.context import FSMContext
from config import *

router = Router()
id_broadcast = -1002033272937


@router.message(Create.photos_ids)
async def create_photos_ids(message: Message, state: FSMContext, album=None):

    if not message.photo and not message.text:
        await message.answer(f"Так дело не идет, фотографии отправляй")
        return
    else:
        photos_ids = []

        if album:
            messages = album
        else:
            messages = [message]
        for element_message in messages:
            await message.bot.download(file=element_message.photo[-1].file_id,
                                       destination=f'photos/{element_message.photo[-1].file_id}.jpg')
            photos_ids.append(element_message.photo[-1].file_id)

        await state.update_data(photos_ids=photos_ids)
        await state.set_state(Create.quantity_of_topics)
        await message.answer(f"Напишите, какое количество тем будет.\n"
                             f"\n"
                             f"<i>Обычно это 30 </i>🤨\n"
                             f"<b>Вопрос 2/4</b>")


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

    if quantity > 100:
        await message.answer(f"Больше 100 быть не может, извини")
        return
    await message.answer(f"Записал. Идем дальше")
    await state.update_data(quantity_of_topics=quantity)
    await state.set_state(Create.people_for_topic)

    await message.answer(f"Напишите, какое количество людей может занимать одну тему.\n"
                         f"\n"
                         f"<i>Обычно это 1 </i>🤨\n"
                         f"<b>Вопрос 3/4</b>")


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

    await message.answer(f"Записал. Идем дальше")
    await state.update_data(people_for_topic=people_for_topic)
    await state.set_state(Create.note)
    await message.answer(f"Напишите дополнительную информацию к брони. "
                         f"Эта информация будет отображена снизу картинок.\n"
                         f"\n"
                         f"<i>Если дополнительной информации нет, нажмите Пропустить </i>🤨\n"
                         f"<b>Вопрос 4/4</b>", reply_markup=next_keyboard)


@router.message(Create.note)
async def leave_note(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(f"Скинь текстом.")
        return

    if message.text.lower() == 'пропустить':
        note = ''
    else:
        note = '\n' + message.text
    await message.answer(f"Значит-ся, все записали.")

    await state.update_data(note=note)
    await state.set_state(Create.okay_bro_yeah_mazafaka)

    await message.answer(f"Вы уверены, что хотите \"открыть бронь\"?", reply_markup=yes_or_no_keyboard)


@router.message(Create.okay_bro_yeah_mazafaka)
async def confidence(message: Message, state: FSMContext):
    if message.text.lower() == 'да, зарегистрировать бронь':
        data = await state.get_data()
        topic_ids = {}
        media = media_group.MediaGroupBuilder()

        with db:
            booking = Booking.create(time_of_creation=datetime.datetime.now(), telegram_id=message.from_user.id,
                                     times_can_choose=data['people_for_topic'])
            for photo_id in data['photos_ids']:
                Photos.create(photo_id=photo_id, booking_id=booking.id)
                media.add_photo(input_file.FSInputFile(f'photos/{photo_id}.jpg'))
            for topic in range(data['quantity_of_topics']):
                topics_db = TopicList.create(time_of_creation=datetime.datetime.now(),
                                 booking_id=booking.id, topic_in_booking_id=topic + 1)
                topic_ids[topics_db.id] = topic+1
        await message.answer('Отправляем в чат фотки...')
        await message.bot.send_media_group(id_broadcast, media.build())

        # <tg-spoiler>Скажем большое спасибо<a href="tg://user?id=1027005788">
        # Александру Викторовичу</a> за разработку бота❤</tg-spoiler>
        msg = await message.bot.send_message(id_broadcast, 'Доброго времени суток, мои любимки!\n'
                                                     f'Разбираем темки! 1 тема = '
                                                     f"<b>{data['people_for_topic']}</b> человек(а)"
                                                     f"{data['note']}\n\n"
                                                     f'Нажмите на кнопку с номером темы, которую Вы решии выбрать по '
                                                           f'фотографии выше. Если тема уже занята, около номера темы'
                                                           f' будет эмодзи ✅. Если Вы передумали и хотите '
                                                           f'взять иную тему, нажмите на номер не занятой темы. '
                                                           f'Если Вы хотите отказаться от темы и не выбирать новую, '
                                                           f'повторно нажмите на кнопку уже выбранной вами темы \n'
                                                           f'\n'
                                                           f'С уважением, '
                                                           f'<a href="tg://user?id={message.from_user.id}>'
                                                           f'{telegram_ids[message.from_user.id].split(' ')[1]}</a>',
                                             reply_markup=builders.create_keyboard(booking.id, topic_ids))
        await message.bot.pin_chat_message(id_broadcast, msg.message_id, False)

        await message.answer('Создано!', reply_markup=ReplyKeyboardRemove())

    elif message.text.lower() == 'нет, сбросить форму':
        await message.answer('Ну и иди нахуй тогда', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('😐')
    await state.clear()
