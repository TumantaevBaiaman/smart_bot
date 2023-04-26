from aiogram import Bot  # импортируем класс Bot из модуля aiogram
from aiogram.dispatcher import Dispatcher  # импортируем класс Dispatcher из модуля aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # импортируем класс MemoryStorage для работы с хранилищем

from config import API_TOKEN_BOT  # импортируем API-токен нашего бота из конфигурационного файла

storage = MemoryStorage()  # создаем объект MemoryStorage для хранения состояний пользователей

bot = Bot(token=API_TOKEN_BOT)  # создаем объект Bot с указанным API-токеном
dp = Dispatcher(bot, storage=storage)  # создаем объект Dispatcher, который будет обрабатывать входящие сообщения, используя указанный бот и хранилище
