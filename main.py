from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

memory = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=memory)

async def on_startup(_):
    await db.db_start()
    print("Бот запущен!")

class NewOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer(f'{message.from_user.full_name}, приветствую в моем магазине')
    await message.answer_sticker('CAACAgIAAxkBAAMWZawtX2xOvVUvQ9iD5V32DJupLNAAAo4AAxZCawq-pIZ9bX4tXDQE',
                                reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор', reply_markup=kb.main_admin)


@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer('Товары в наличии: ',
                         reply_markup=kb.catalog_list)

@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer('Корзина пуста')

@dp.message_handler(text='Контакты')
async def contact(message: types.Message):
    await message.answer('По всем вопросам обращаться: @xccyrate')

@dp.message_handler(text='Админ-панель')
async def admin(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в панель администратора!', reply_markup=kb.admin_panel)
    else:
        await message.reply('Я не понимаю, напиши команду!')


@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await NewOrder.type.set()
        await message.answer(f'Выберите тип товара: ', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я не понимаю, напиши команду!')

@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer('Напишите название товара', reply_markup=kb.cancel)
    await NewOrder.next()

@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Напишите описание товара')
    await NewOrder.next()


@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer('Напишите цену товара')
    await NewOrder.next()

@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте фотографию товара')
    await NewOrder.next()


@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')

@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_item(state)
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


#@dp.message_handler(commands=['id'])
#async def cmd_id(message: types.Message):
#    await message.answer(f'{message.from_user.id}')




@dp.message_handler(content_types=['document', 'photo', 'sticker', 'text'])
async def forward_message(message: types.Message):
    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)

#@dp.message_handler(content_types=['document', 'photo', 'sticker'])
#async def forward(message: types.Message):
#    await bot.send_message(message.from_user.id, message.chat.id)


#@dp.message_handler(content_types=['sticker'])
#async def user_stick(message: types.Message):
#    await message.reply(message.sticker.file_id)

@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.callback_query):
    if callback_query.data == 'nike':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товары бренда "Nike" в наличии: ')
    if callback_query.data == 'adidas':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товары бренда "Adidas" в наличии: ')
    if callback_query.data == 'vans':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Товары бренда "Vans" в наличии: ')

@dp.message_handler()
async def cmd_other(message: types.Message):
    await message.reply('Я не понимаю, напиши команду!')
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)




