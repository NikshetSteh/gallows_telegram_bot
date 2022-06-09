from aiogram import Bot, types

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from data import replicas
import user
import loader

from datetime import datetime

import logging

import config

file_log = logging.FileHandler("logs\logs.log")
console_out = logging.StreamHandler()

logging.basicConfig(handlers = (file_log, console_out), level = logging.INFO)

bot = Bot(token = config.TOKEN)
dispatcher = Dispatcher(bot)

users = {}

@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if not message.from_user.id in users:
        logging.info(f"creat new acount: {message.from_user.id}")
        users.update({message.from_user.id: user.User(message.from_user.id)})
    await message.answer(replicas.REPLICAS_HELLO, reply_markup = user.main_keybord)

@dispatcher.message_handler(commands=['help', 'помощь'])
async def help(message: types.Message):
    await message.answer(replicas.REPLICAS_HELP)

@dispatcher.message_handler(commands=['start_game', 'новая_игра'])
async def start_new_game(message: types.Message):
    await users[message.from_user.id].start_game(message)

@dispatcher.message_handler(commands=['статистика'])
async def start_new_game(message: types.Message):
    await users[message.from_user.id].print_statistics(message)


@dispatcher.message_handler()
async def get_new_message(message: types.Message):
    if not message.from_user.id in users:
        logging.info(f"creat new acount: {message.from_user.id}")
        users.update({message.from_user.id: user.User(message.from_user.id)})

    await users[message.from_user.id].get_message(message)

loader.Loader.load(users)

user.load_words("data/")

logging.info(f"====={datetime.now()}=====")

if not config.USE_WEBHOOK:
    executor.start_polling(dispatcher, skip_updates = True)
else:
    async def on_startup(dispatcher):
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates = True)


    async def on_shutdown(dispatcher):
        await bot.delete_webhook()

    start_webhook(
        dispatcher = dp,
        webhook_path = WEBHOOK_PATH,
        skip_updates = True,
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        host = WEBAPP_HOST,
        port = WEBAPP_PORT,
    )

loader.Loader.save(users.values())