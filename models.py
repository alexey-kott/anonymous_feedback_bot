from random import choice

from aiogram.types import Message, CallbackQuery
from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField, IntegrityError, ForeignKeyField


class BaseClass(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite3')


class Chat(BaseClass):
    name = TextField()
    last_message_id = IntegerField()

    @classmethod
    def get_by_message(cls, message: Message):
        try:
            chat, created = Chat.get_or_create(id=message.chat.id,
                                               name=message.chat.full_name,
                                               last_message_id=message.message_id)
        except IntegrityError:
            chat = Chat.get(id=message.chat.id)

        chat.last_message_id = message.message_id
        chat.save()

        return chat

    @classmethod
    def get_by_callback(cls, callback: CallbackQuery):

        return Chat.get(id=callback.message.chat.id)


class User(BaseClass):
    username = TextField()
    first_name = TextField()
    last_name = TextField(null=True)

    @classmethod
    def get_by_message(cls, message: Message):
        user, created = User.get_or_create()


class Animal(BaseClass):
    name = TextField()
    user = ForeignKeyField(User, backref='animals')

    @staticmethod
    def get_random():
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
