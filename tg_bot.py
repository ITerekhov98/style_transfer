import asyncio
import os
import shutil
import logging
from typing import List

from environs import Env
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram_media_group import media_group_handler
from aiogram.types import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logging.handlers import RotatingFileHandler

from style_transfer import get_style_transferred_photo


logger = logging.getLogger(__name__)

EXAMPLES_DIR = 'examples/'
img_order = {'content': 0, 'style': 1, 'result': 2}


class BotStates(StatesGroup):
    waiting_for_photos = State()


async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Хочу перенести стиль на фото")
    button_2 = types.KeyboardButton(text="Покажи примеры своих скиллов")
    keyboard.add(button_1, button_2)
    await message.answer('Привет! Чем могу помочь?', reply_markup=keyboard)


async def show_examples(message):
    for root, dirs, images in os.walk(EXAMPLES_DIR):
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        for image in sorted(images, key=lambda x: img_order[x.split('.')[0]]):
            path_img = f'{root}/{image}'
            media.attach_photo(types.InputFile(path_img), image[:-4])
        if images:
            await message.reply_media_group(media=media)


async def handle_style_transfer(message):
    await message.answer(
        '''Окей, всё что тебе нужно это прислать мне 2 фото:
        1 послужит примером стиля, а на второй я постараюсь
        его перенести. Не перепутай )'''
    )
    await BotStates.waiting_for_photos.set()


@media_group_handler
async def download_photo(messages: List[types.Message], state: FSMContext):
    images = []
    for message in messages:
        buffer = await message.photo[-1].download(
            destination_dir=f"users/{message.chat.id}"
        )
        images.append(buffer.name)
    photos_dir = os.path.split(buffer.name)[0]
    await message.answer('Принял. Дай мне 2-3 минуты')
    logger.info(f'Proccess photos from user {message.chat.id}...')
    try:
        styled_photo_path = get_style_transferred_photo(photos_dir, images)
    except Exception as err:
        logger.error(err, exc_info=True)
        await message.answer('Что-то пошло не так. Попробуй пожалуйста ещё раз')
        return

    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    media.attach_photo(types.InputFile(styled_photo_path))
    await message.reply_media_group(media=media)
    logger.info(f'Success')
    shutil.rmtree(photos_dir)
    await state.finish()


async def main():
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename = "logfile.log",
        format = Log_Format, 
        level = logging.INFO
    )
    handler = RotatingFileHandler(
        "logfile.log",
        maxBytes=100000,
        backupCount=2
    )
    logger.addHandler(handler)

    env = Env()
    env.read_env()
    bot = Bot(token=env.str('TG_BOT_TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(
        show_examples,
        lambda message: message.text == 'Покажи примеры своих скиллов',
        state="*"
    )
    dp.register_message_handler(
        handle_style_transfer,
        lambda message: message.text == "Хочу перенести стиль на фото",
        state="*"
    )
    dp.register_message_handler(
        download_photo,
        MediaGroupFilter(is_media_group=True),
        content_types=ContentType.PHOTO,
        state=BotStates.waiting_for_photos
    )
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
