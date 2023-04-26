# Импорт необходимых классов для создания клавиатуры
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

# Создание кнопок клавиатуры
b1 = KeyboardButton('🌍узнать погоду') # Кнопка для получения информации о погоде
b2 = KeyboardButton('💱конвертировать') # Кнопка для конвертации валюты
b3 = KeyboardButton('🥰картинку') # Кнопка для получения изображения
b4 = KeyboardButton('📄создавать опросы') # Кнопка для создания опросов

# Создание клавиатуры и добавление кнопок
menu_info = ReplyKeyboardMarkup(resize_keyboard=True) # Создание объекта клавиатуры
menu_info.add(b1, b2).add(b3, b4) # Добавление кнопок в клавиатуру