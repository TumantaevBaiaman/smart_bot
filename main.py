# Импортируем объект dp из модуля bot
from bot import dp

# Импортируем функцию executor из модуля aiogram.utils
from aiogram.utils import executor

# Импортируем модули с обработчиками событий
from handlers import logic_weather, logic_convert, logic_cute_animals, logic_quiz, commands

# Регистрируем команды для администраторов
commands.register_admin(dp)

# Регистрируем обработчик погоды
logic_weather.register_weather(dp)

# Регистрируем обработчик конвертации единиц измерения
logic_convert.register_convert(dp)

# Регистрируем обработчик симпатичных животных
logic_cute_animals.register_cute_animals(dp)

# Регистрируем обработчик викторин
logic_quiz.register_quiz(dp)

# Запускаем бесконечный цикл опроса бота
# skip_updates=True говорит боту пропускать необработанные обновления, если такие есть
executor.start_polling(dp, skip_updates=True)
