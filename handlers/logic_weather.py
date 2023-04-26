
import aiohttp
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from bot import bot
from config import API_KEY_WEATHER, WEATHER_API_URL
from aiogram.dispatcher.filters.state import StatesGroup, State


class StateWeather(StatesGroup):
    city = State()


async def start_weather(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет, укажи город')
    await StateWeather.city.set()


async def get_weather(message: types.Message, state: StateWeather):
    city = message.text
    api_key = API_KEY_WEATHER
    url = WEATHER_API_URL.format(city=city, api_key=api_key)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                weather_data = await response.json()
                weather_main = weather_data['weather'][0]['main']
                weather_description = weather_data['weather'][0]['description']
                temp = weather_data['main']['temp']
                await bot.send_message(message.from_user.id, f'Текущая погода в {city}:\n{weather_main}, {weather_description}\nТемпература: {temp}°C')
                await state.finish()
        except:
            await bot.send_message(message.from_user.id, 'Увы, Вы ввели название города неправильно.')
            await StateWeather.city.set()


def register_weather(dp : Dispatcher):
    # Регистрация обработчиков сообщений для создания опроса
    dp.register_message_handler(start_weather, Text(equals='🌍узнать погоду', ignore_case=True))
    dp.register_message_handler(get_weather, state=StateWeather.city)