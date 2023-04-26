
import aiohttp
from aiogram import types, Dispatcher
from bot import dp, bot
from key.button_menu import menu_info


async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Я умный бот, готовый помочь вам в чем-то. Чем я могу быть полезен?', reply_markup=menu_info)


def register_admin(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
