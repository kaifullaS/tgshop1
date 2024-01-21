from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton



main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add('Создать промокод')

catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Nike', callback_data='nike'),
                InlineKeyboardButton(text='Adidas', callback_data='adidas'),
                InlineKeyboardButton(text='Vans', callback_data='vans'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')