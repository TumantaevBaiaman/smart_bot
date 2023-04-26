
import aiohttp
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from bot import bot
from config import EXCHANGE_RATES_API_URL, API_KEY_EXCHANGE_RATES
from aiogram.dispatcher.filters.state import StatesGroup, State


class StateConvert(StatesGroup):
    from_currency = State()  # Состояние "из какой валюты конвертировать"
    to_currency = State()  # Состояние "в какую валюту конвертировать"
    amount = State()  # Состояние "какая сумма конвертирования"


async def start_convert_currency(message: types.Message):
    await bot.send_message(message.from_user.id, 'Укажите из какой валюты хотите конверт')
    await StateConvert.from_currency.set()


async def get_from_currency(message: types.Message, state: StateConvert):
    data_from_currency = message.text.upper()
    async with aiohttp.ClientSession() as session:
        headers = {"apikey": API_KEY_EXCHANGE_RATES}
        url = f'{EXCHANGE_RATES_API_URL}latest?symbols=&base='
        async with session.get(url, headers=headers) as response:
            available_currencies_data = await response.json()
            available_currencies = available_currencies_data['rates'].keys()  # Получаем доступные валюты
        if data_from_currency not in available_currencies:  # Проверяем, что введенная валюта существует
            await message.reply(
               'Указанных валюта не существует. Пожалуйста, убедитесь, что вы ввели правильные коды валют.')
            await StateConvert.from_currency.set()
        else:
            async with state.proxy() as data:
                data["from_currency"] = data_from_currency
                await bot.send_message(message.from_user.id, 'Отлично теперь укажите на какую валюту конвертировать')
                await StateConvert.to_currency.set()


async def get_to_currency(message: types.Message, state: StateConvert):
    data_to_currency = message.text.upper()
    async with aiohttp.ClientSession() as session:
        headers = {"apikey": API_KEY_EXCHANGE_RATES}
        url = f'{EXCHANGE_RATES_API_URL}latest?symbols=&base='
        async with session.get(url, headers=headers) as response:
            available_currencies_data = await response.json()
            available_currencies = available_currencies_data['rates'].keys()  # Получаем доступные валюты
        if data_to_currency not in available_currencies:  # Проверяем, что введенная валюта существует
            await message.reply(
               'Указанных валюта не существует. Пожалуйста, убедитесь, что вы ввели правильные коды валют.')
            await StateConvert.to_currency.set()
        else:
            async with state.proxy() as data:
                data["to_currency"] = data_to_currency
                await bot.send_message(message.from_user.id, 'Отлично теперь укажите сумму')
                await StateConvert.amount.set()


async def get_amount(message: types.Message, state: StateConvert):
    data_amount = message.text
    if data_amount.isdigit(): # Проверяем, что введенные данные являются числом
        async with aiohttp.ClientSession() as session:
            headers = {"apikey": API_KEY_EXCHANGE_RATES}
            async with state.proxy() as data:
                # Формируем URL для запроса к API
                url = f"{EXCHANGE_RATES_API_URL}convert?to={data['to_currency']}&from={data['from_currency']}&amount={data_amount}"
                async with session.get(url, headers=headers) as response: # Получаем данные о курсе валют
                    exchange_rates_data = await response.json()
                    result = exchange_rates_data['result']
                    # Отправляем сообщение с результатом конвертации
                    await bot.send_message(message.from_user.id, f"{data_amount} {data['from_currency']} 💱 -> {result} {data['to_currency']}")
                    await state.finish()

    else:
        # Если введенные данные не являются числом, отправляем сообщение с просьбой ввести данные еще раз
        await bot.send_message(message.from_user.id, "Вы ввели некорректные данные, пожалуйста, попробуйте еще раз.")
        # Возвращаемся к состоянию получения суммы
        await StateConvert.amount.set()


def register_convert(dp : Dispatcher):
    # Регистрация обработчиков сообщений для создания опроса
    dp.register_message_handler(start_convert_currency, Text(equals='💱конвертировать', ignore_case=True))
    dp.register_message_handler(get_from_currency, state=StateConvert.from_currency)
    dp.register_message_handler(get_to_currency, state=StateConvert.to_currency)
    dp.register_message_handler(get_amount, state=StateConvert.amount)


