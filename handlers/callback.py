import datetime

import aiogram.exceptions
from aiogram.types import CallbackQuery
from model_db import *
from config import telegram_ids
from aiogram.types import FSInputFile
from handlers import builders

joke = True


async def select_topic(call: CallbackQuery):
    booking_id = int(call.data.split(',')[0])
    topic = int(call.data.split(',')[1])
    user_id = call.from_user.id
    name = telegram_ids[user_id].split(' ')[1]

    topic_note_telegram_id = []
    with db:
        topic_note = UserList().select().where(UserList.topic_id == topic)
        for note in topic_note:
            topic_note_telegram_id.append(note.telegram_id)
        booking_note = Booking().select().where(Booking.id == booking_id)
        for note in booking_note:
            times_can_choose = note.times_can_choose
        topic_note2 = TopicList().select().where(TopicList.id == topic)
        for note in topic_note2:
            humanreadable_topic = note.topic_in_booking_id
    if user_id in topic_note_telegram_id:
        # await call.answer(f'Вы уже заняли эту тему. Если вы хотите изменить тему, '
                          # f'нажмите на кнопку свободной темы', True)
        with db:
            UserList().delete().where(UserList.topic_id == topic).execute()
            topic_note = TopicList().select().where(TopicList.id == topic)
            for note2 in topic_note:
                humanreadable_topic2 = note2.topic_in_booking_id
            await call.bot.send_message(call.message.chat.id,
                                            f'<a href="tg://user?id={user_id}">{name}</a> '
                                            f'больше не занимает тему {humanreadable_topic2}',
                                            reply_to_message_id=call.inline_message_id)
        topic_ids = {}
        busies = []
        topic_bd = TopicList().select().where(TopicList.booking_id == booking_id)
        for topic in topic_bd:
            topic_ids[topic.id] = topic.topic_in_booking_id

        user_bd = UserList().select().where(UserList.booking_id == booking_id)
        temp = []
        for note in user_bd:
            temp.append(note.topic_id)
        for topic_id in temp:
            if temp.count(topic_id) == times_can_choose:
                busies.append(topic_id)
        try:
            await call.message.edit_reply_markup(call.inline_message_id,
                                                 reply_markup=builders.create_keyboard(booking_id, topic_ids, busies))
        except aiogram.exceptions.TelegramBadRequest:
            pass
        await call.answer()

        return
    if len(topic_note) == times_can_choose:
        students = ''
        for i in topic_note_telegram_id:
            students += telegram_ids[i].split(' ')[0] + ' ' + telegram_ids[i].split(' ')[1] + ', '
        else:
            students = students[:-2]
        if joke:
            await call.bot.send_voice(call.message.chat.id, FSInputFile(f'zanato.ogg'),
                                      caption=f'<a href="tg://user?id={user_id}">{name}</a>, '
                                              f'{students} так не дума(ет/ют)')
        else:
            await call.answer(f'Выбраная тема занята следующим(и) одногруппник(ом/ами): {students}', True)
        return
    else:
        with db:
            user_db = UserList().select().where(UserList.booking_id
                                                == booking_id).where(UserList.telegram_id == user_id)
            if len(user_db) == 1:
                for note in user_db:
                    UserList().delete().where(UserList.id == note.id).execute()
                    topic_note2 = TopicList().select().where(TopicList.id == note.topic_id)
                    for note2 in topic_note2:
                        humanreadable_topic2 = note2.topic_in_booking_id
                    await call.bot.send_message(call.message.chat.id,
                                                f'<a href="tg://user?id={user_id}">{name}</a> '
                                                f'больше не занимает тему {humanreadable_topic2}',
                                                reply_to_message_id=call.inline_message_id)
            UserList().create(time_of_creation=datetime.datetime.now(), topic_id=topic,
                              telegram_id=user_id, booking_id=booking_id)
            topic_ids = {}
            busies = []
            topic_bd = TopicList().select().where(TopicList.booking_id == booking_id)
            for topic in topic_bd:
                topic_ids[topic.id] = topic.topic_in_booking_id

            user_bd = UserList().select().where(UserList.booking_id == booking_id)
            temp = []
            for note in user_bd:
                temp.append(note.topic_id)
            for topic_id in temp:
                if temp.count(topic_id) == times_can_choose:
                    busies.append(topic_id)

        await call.bot.send_message(call.message.chat.id,
                                    f'<a href="tg://user?id={user_id}">{name}</a> занял тему {humanreadable_topic}',
                                    reply_to_message_id=call.inline_message_id)
        try:
            await call.message.edit_reply_markup(call.inline_message_id,
                                                 reply_markup=builders.create_keyboard(booking_id, topic_ids, busies))
        except aiogram.exceptions.TelegramBadRequest:
            pass

    await call.answer()
