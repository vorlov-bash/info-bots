from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from src.services.repository import Repo
from .messages import INFO_ABOUT_ME

callback_factory = CallbackData('hellop', '@')
print(callback_factory.new('hello'))


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='About me')
    )

    await m.reply("Hello, I'm that one of the few bots written on Python programming language. 💪🏻\n"
                  "Click some buttons to get info about ℹ️.")


async def info_about_me_button(m: Message):
    await m.reply(INFO_ABOUT_ME)


async def info_about_bots_on_python(m: Message):
    await m.reply("""To start learning python and write bots on it, click some links from my list:
                  * https://www.learnpython.org/
                  * https://docs.quantifiedcode.com/python-anti-patterns/
                  * https://mastergroosha.github.io/telegram-tutorial/""")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=['start'], state='*')
