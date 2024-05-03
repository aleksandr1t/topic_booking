from peewee import SqliteDatabase
from peewee import Model

from peewee import PrimaryKeyField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import CharField
from peewee import BooleanField
from peewee import DecimalField

db = SqliteDatabase('telegram.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Booking(BaseModel):
    time_of_creation = DateTimeField()
    telegram_id = IntegerField()
    times_can_choose = IntegerField()

    class Meta:
        db_table = 'bookings'


class Photos(BaseModel):
    photo_id = IntegerField()
    booking_id = IntegerField()

    class Meta:
        db_table = 'photos'


class TopicList(BaseModel):
    time_of_creation = DateTimeField()
    booking_id = IntegerField()
    topic_in_booking_id = IntegerField()

    class Meta:
        db_table = 'topics'


class UserList(BaseModel):
    time_of_creation = DateTimeField()
    topic_id = IntegerField()
    telegram_id = IntegerField()

    class Meta:
        db_table = 'users'


if __name__ == "__main__":
    db.create_tables([Booking, Photos, TopicList, UserList])
