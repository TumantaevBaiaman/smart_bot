from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

b2 = KeyboardButton('отправить группу')

quiz_btn = ReplyKeyboardMarkup(resize_keyboard=True)
quiz_btn.add(b2)