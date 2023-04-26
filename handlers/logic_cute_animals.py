import os
import random

from aiogram.dispatcher.filters import Text

from bot import bot
from aiogram import types
from aiogram import types, Dispatcher

# Определяем путь к папке с изображениями
IMAGES_DIR = 'images/cute_animals'

# Получаем список файлов в папке
image_files = os.listdir(IMAGES_DIR)


async def post_cute_animals(message: types.Message):
    await bot.send_message(message.from_user.id, 'Отлично немного подождите\n🐶 🐱 🐭 🐹 🐰 🦊 🐻 🐼 🐻‍ 🐨 🐯 🦁 🐮 🐣 🐥 🦆 🦅 🦉')
    # Выбираем случайный файл из списка
    random_image = random.choice(image_files)
    with open(os.path.join(IMAGES_DIR, random_image), 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id, photo=types.InputFile(photo))


def register_cute_animals(dp : Dispatcher):
    # Регистрация обработчиков сообщений для создания опроса
    dp.register_message_handler(post_cute_animals, Text(equals='🥰картинку', ignore_case=True))