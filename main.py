import os
import sys
import re
import logging
import configparser
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Regexp
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db_pos_map import Base, SnOfPos
import strings as bot_str
from utils import TestStates

conf = configparser.RawConfigParser()
try:
    conf.read('./cnf/config.cnf')
except Exception as e:
    print(e)

# API_TOKEN = conf.get('Bot', 'API_TOKEN') #1496305081:AAFki0-xalp2Bg_au19_1vIg7gZjz1jAgXo
API_TOKEN = '5145769334:AAE1Eaf7_2tPHWEkYCQ2Pl9Fdn_24mhDqUs'
# chat_id = conf.get('Bot', 'chat_id')
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())

DB_FILENAME = conf.get('Sql', 'DB_FILENAME')
admin_id = conf.get('Bot', 'admin_id')
engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
# lambda message: message.text == '/start'

@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message):
    # print(message.author_signature)
    state = dp.current_state(user=message.from_user.id)
    await message.reply(f' Вітаю {message.from_user.first_name}  \n{bot_str.start_cmd_string}')
    photo = open('./img/PN_of_POS.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo, caption=bot_str.pos_photo_string)
    await state.set_state(TestStates.all()[1])


POS_SN_VX520 = r'^\d{9}'
POS_PN_X_990 = r'^V\w\w\w\w\w\w\w\w\w'


@dp.message_handler(state=TestStates.TEST_STATE_1)
async def read_SN(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    VX520 = re.search(POS_SN_VX520, message.text)
    X990 = re.search(POS_PN_X_990, message.text)
    print(VX520[0] if VX520 else 'Not_found')
    print(X990[0] if X990 else 'Not_found')
    if VX520:
        await message.reply(f'Ви ввели серійний номер: {message.text[0:3]}-{message.text[3:6]}-{message.text[6:9]}\n'
                            f'Модель термінала: VX520')
        await state.set_state(TestStates.all()[2])
    elif X990:
        await message.reply(f'Ви ввели серійний номер: {message.text}\n'
                            f'Модель термінала: X990')
        await state.set_state(TestStates.all()[3])
    else:
        await message.reply(f'Введено некоректні данні.\n Перевірте введений серійний номер ! \n')



@dp.message_handler(state ='*', commands=['register'])
async def add_new(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.reply(f'Щоб додати новий терімінал до БД введіть спочатку модель(VX520, X990),\n а наступним повідомленням серійний '\
                        f'номер \n')
    await state.set_state(TestStates.all()[6])


@dp.message_handler(state=TestStates.TEST_STATE_ADD)
async def read_model(message: types.Message):
    state = dp.current_state(user=message.from_user.id)

    VX520 = re.search('VX520', message.text)
    X990 = re.search('X990', message.text)
    print(VX520[0] if VX520 else 'Not_found')
    print(X990[0] if X990 else 'Not_found')
    if VX520:
        await message.reply(f'Ви ввели серійний номер: {message.text[0:3]}-{message.text[3:6]}-{message.text[6:9]}\n'
                            f'Модель термінала: VX520')
        await state.set_state(TestStates.all()[2])
    elif X990:
        await message.reply(f'Ви ввели серійний номер: {message.text}\n'
                            f'Модель термінала: X990')
        await state.set_state(TestStates.all()[3])
    else:
        await message.reply(f'Введено некоректні данні.\n Перевірте введений серійний номер ! \n')







@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = message.document.file_name
    path_to_save = f'./data/files/{filename}'
    await bot.download_file(file_path, path_to_save)
    await message.reply(f'Файл {filename} успішно збережено \n')




@dp.channel_post_handler()
async def reply_to_new_post(message: types.Message):
    await message.reply(f'Get new message in my channel {message.text} brrr, send here all sorts')
    print(f'get message {message} \n ')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
