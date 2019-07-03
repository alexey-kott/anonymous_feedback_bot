import logging
from asyncio import sleep

import requests
from aiohttp import BasicAuth
from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from requests.exceptions import ConnectionError
from googletrans import Translator

from config import BOT_TOKEN, PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USERNAME
from models import Chat, User, Msg, UserHashMatching

logging.basicConfig(level=logging.INFO)
translator = Translator()

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
    Msg.create_table(fail_silently=True)
    UserHashMatching.create_table(fail_silently=True)


@dp.message_handler(commands=['ping'])
async def ping_handler(message: Message):
    await message.reply("I'm alive")


@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    await message.reply("Привет! Этот бот создан для сбора анонимного фидбэка. "
                        "Отправь мне любое сообщение и оно будет переслано в чат без указания твоего имени.")


@dp.message_handler(commands=['author', 'about', 'info'])
async def ping_handler(message: Message):
    await message.reply("По вопросам создания ботов обращаться к @alexkott")


@dp.message_handler(content_types=[ContentType.ANY])
async def message_handler(message: Message):
    mode = message.chat.type
    Chat.save_chat(message)
    user = User.get_by_message(message)
    Msg.create(text=message.text, user=user, mode=mode)

    if mode == 'private':
        for chat in Chat.select():
            sender_title = translator.translate(f"Unidentified {user.animal} writes:", dest='ru', src='en').text
            msg_text = f"*{sender_title}* \n{message.text}"

            inline_keyboard = InlineKeyboardMarkup()
            inline_button = InlineKeyboardButton('Ответить в боте', switch_inline_query=f'Ответить {user.animal}:')
            inline_keyboard.add(inline_button)
            await bot.send_message(chat_id=chat.id, text=msg_text, parse_mode='Markdown', reply_markup=inline_keyboard)
            await sleep(1)


if __name__ == "__main__":
    init()
    executor.start_polling(dp)
