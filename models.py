import time
from datetime import datetime, timedelta
from random import choice, randint
import hashlib

from aiogram.types import Message
from peewee import SqliteDatabase, Model, TextField, DateTimeField, ForeignKeyField, fn, IntegerField


class BaseClass(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite3')


class Chat(BaseClass):
    name = TextField()

    @classmethod
    def save_chat(cls, message: Message):
        if message.chat.type != 'private':
            Chat.get_or_create(id=message.chat.id,
                               name=message.chat.full_name)


class User(BaseClass):
    username = TextField(null=True)
    first_name = TextField()
    last_name = TextField(null=True)
    animal = TextField()

    @classmethod
    def get_by_message(cls, message: Message) -> 'User':
        try:
            user = User.get(id=message.from_user.id)
            user.reborn()
        except Exception:
            from_user = message.from_user
            user = User.create(id=from_user.id,
                               username=from_user.username,
                               first_name=from_user.first_name,
                               last_name=from_user.last_name if from_user.last_name else '',
                               animal=User.get_animal())
            UserHashMatching.acquire(user.id)

        return user

    @classmethod
    def get_animal(cls) -> str:
        animal_list = ['Alligator', 'Anteater', 'Armadillo', 'Auroch', 'Axolotl', 'Badger', 'Bat', 'Bear', 'Beaver',
                       'Buffalo', 'Camel', 'Capybara', 'Chameleon', 'Cheetah', 'Chinchilla', 'Chipmunk', 'Chupacabra',
                       'Cormorant', 'Coyote', 'Crow', 'Dingo', 'Dinosaur', 'Dog', 'Dolphin', 'Duck', 'Elephant',
                       'Ferret', 'Fox', 'Frog', 'Giraffe', 'Gopher', 'Grizzly', 'Hedgehog', 'Hippo', 'Hyena', 'Ibex',
                       'Ifrit', 'Iguana', 'Jackal', 'Kangaroo', 'Koala', 'Kraken', 'Lemur', 'Leopard', 'Liger', 'Lion',
                       'Llama', 'Loris', 'Manatee', 'Mink', 'Monkey', 'Moose', 'Narwhal', 'NyanCat', 'Orangutan',
                       'Otter', 'Panda', 'Penguin', 'Platypus', 'Pumpkin', 'Python', 'Quagga', 'Rabbit', 'Raccoon',
                       'Rhino', 'Sheep', 'Shrew', 'Skunk', 'Squirrel', 'Tiger', 'Turtle', 'Walrus', 'Wolf', 'Wolverine',
                       'Wombat']

        return choice(animal_list)

    def reborn(self):
        last_message_dt = Msg.select(Msg.dt, fn.MAX(Msg.dt)).where(Msg.user == self).scalar()

        if last_message_dt < datetime.now() - timedelta(hours=1):
            self.animal = User.get_animal()
            self.save()

            UserHashMatching.acquire(self.id)


class UserHashMatching(BaseClass):  # using anonymously for answering user via bot
    user_hash = IntegerField()
    user = ForeignKeyField(User, backref='hashes')
    dt = DateTimeField(default=datetime.now)

    @classmethod
    def acquire(cls, user_id: int):
        unixtime = int(time.time())
        hash_object = hashlib.sha256()
        hash_object.update(f"{unixtime}{user_id}{randint(1, 10**10)}")
        user_hash = hash_object.hexdigest()
        print(user_hash)
        UserHashMatching.create(user_hash=user_hash, user=user_id)


class Msg(BaseClass):
    dt = DateTimeField(default=datetime.now)
    text = TextField(null=True)
    user = ForeignKeyField(User, backref='messages')
    mode = TextField()
