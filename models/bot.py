import os, dotenv

from aiogram import Bot, Dispatcher


def create():
    dotenv.load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    return bot, dp
