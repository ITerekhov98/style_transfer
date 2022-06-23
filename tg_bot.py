import logging
from aiogram import Bot, Dispatcher, executor, types

from environs import Env


logger = logging.getLogger(__name__)




async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Хочу перенести стиль на фото")
    button_2 = types.KeyboardButton(text="Покажи примеры своих скиллов")
    keyboard.add(button_1, button_2)
    await message.answer('Привет! Чем могу помочь?', reply_markup=keyboard)

async def show_examples(message):
    await message.answer(1)


async def handle_style_transfer(message):
    await message.answer('Окей, всё что тебе нужно это прислать мне 2 фото: 1 послужит примером стиля, а на второй я постараюсь его перенести. Не перепутай )')

def main():
    logger.setLevel(logging.INFO)
    env = Env()
    env.read_env()
    bot = Bot(token=env.str('TG_BOT_TOKEN'))  
    dp = Dispatcher(bot)
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(show_examples, lambda message: message.text == 'Покажи примеры своих скиллов')
    dp.register_message_handler(handle_style_transfer, lambda message: message.text == "Хочу перенести стиль на фото")
    executor.start_polling(dp, skip_updates=True)



if __name__ == "__main__":
    main()