import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.utils import executor
import requests
from aiohttp import BasicAuth

from config import BOT_TOKEN, PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USERNAME

from models import Chat, User

logging.basicConfig(level=logging.INFO)

try:
    PROXY_AUTH = None
    PROXY_URL = None
    response = requests.get('https://api.telegram.org')
except ConnectionError as e:
    PROXY_URL = f"socks5://{PROXY_HOST}:{PROXY_PORT}"
    PROXY_AUTH = BasicAuth(login=PROXY_USERNAME, password=PROXY_PASS)
bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)


def init():
    Chat.create_table(fail_silently=True)
    User.create_table(fail_silently=True)


@dp.message_handler(commands=['ping'])
async def ping_handler(message: Message):
    await message.reply("I'm alive")


@dp.message_handler(content_types=[ContentType.ANY])
async def message_handler(message: Message):
    chat =
    for chat in Chat.select():
        print(chat)


if __name__ == "__main__":
    init()
    executor.start_polling(dp)