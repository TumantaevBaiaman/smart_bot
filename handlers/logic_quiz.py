from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, Poll, PollOption
from aiogram.utils import executor
from bot import bot
from aiogram.dispatcher.filters.state import StatesGroup, State

from key.button_menu import menu_info
from key.button_quiz import quiz_btn


class StateQuiz(StatesGroup):
    question = State()  # Состояние, на котором мы ждем вопрос для нового опроса
    answers = State()  # Состояние, на котором мы ждем варианты ответов на вопрос
    group = State()  # Состояние, на котором мы ждем название группы, в которую мы отправим опрос


async def start_quiz(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пожалуйста, введите вопрос для нового опроса')
    await StateQuiz.question.set()  # Установка текущего состояния на "question"


async def get_question(message: types.Message, state=StateQuiz):
    question = message.text
    async with state.proxy() as data:
        data['question'] = question  # Сохраняем вопрос в словарь "data"
        await bot.send_message(message.from_user.id, 'Добавить вариант ответа на вопрос')
        await StateQuiz.answers.set()  # Переключаемся на состояние "answers"


async def get_answer(message: types.Message, state=StateQuiz):
    answer = message.text
    if answer != 'отправить группу':  # Если ответ не является командой отправки группе
        async with state.proxy() as data:
            answers = data.get('answers', [])  # Получаем список ответов из словаря "data"
            answers.append(answer)  # Добавляем текущий ответ в список ответов
            data['answers'] = answers  # Сохраняем список ответов в словарь "data"
        await message.answer(f'Вариант ответа "{answer}" добавлен в список. Выберите, что хотите сделать дальше:', reply_markup=quiz_btn)  # Отправляем сообщение с кнопками управления опросом
    else:  # Если ответ является командой отправки группе
        async with state.proxy() as data:
            if len(data["answers"])>=2:  # Если список ответов содержит не менее двух ответов
                await message.answer(f'Пожалуйста, введите название группы в формате @название_группы')
                await StateQuiz.group.set()  # Переключаемся на состояние "group"
            else:  # Если список ответов содержит менее двух ответов
                await message.answer(f'Уважаемый пользователь, к сожалению, ваш выбор слишком ограничен. Пожалуйста, добавьте больше вариантов ответов, чтобы улучшить опрос.')


async def send_group(message: types.Message, state=StateQuiz):
    group = message.text

    # Обработка ошибок и отправка опроса
    try:
        async with state.proxy() as data:
            # Создание опроса на основе полученных данных
            poll = types.Poll(
                type=types.PollType.REGULAR,
                question=data["question"],  # вопрос опроса
                options=data["answers"],  # варианты ответов
            )
            # Отправка сообщения пользователю об отправке опроса в группу
            await message.answer(f'Опрос был отправлен группу {group}')
            # Отправка опроса в группу
            await bot.send_poll(group, question=poll.question, options=poll.options, type=poll.type)
            # Отправка сообщения пользователю об успешной отправке опроса и переход к главному меню
            await message.answer(f'Отлично', reply_markup=menu_info)
            # Завершение состояния
            await state.finish()

    # Обработка исключений и отправка сообщения об ошибке
    except:
        await message.answer(f'Ошибка, причины\n1)Убедитесь, что вы правильно указали '
                             f'идентификатор группового чата в методе добавления бота в группу. '
                             f'Убедитесь, что идентификатор группы указан в правильном формате.\n2)Проверьте, что название группы указано правильно, и что бот действительно не был добавлен в группу. В случае ошибки с названием группы, '
                             f'попробуйте указать идентификатор группы вместо названия.\n3)Проверьте, существует ли группа. Если группа не существует, создайте новую группу и попробуйте добавить бота еще раз.\n4)'
                             f'Убедитесь, что ваш бот имеет права администратора в групповом чате. Если у вашего бота нет необходимых прав, он не сможет присоединиться к группе.\n'
                             f'Если вы все еще не можете добавить бота в групповой чат, попробуйте связаться со службой поддержки мессенджера, в котором вы используете бота, для получения дополнительной помощи.',
                             reply_markup=None)
        # Переход к состоянию ожидания выбора группы
        await StateQuiz.group.set()


def register_quiz(dp : Dispatcher):
    # Регистрация обработчиков сообщений для создания опроса
    dp.register_message_handler(start_quiz, Text(equals='📄создавать опросы', ignore_case=True))
    dp.register_message_handler(get_question, state=StateQuiz.question)
    dp.register_message_handler(get_answer, state=StateQuiz.answers)
    dp.register_message_handler(send_group, state=StateQuiz.group)