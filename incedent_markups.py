import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from markups import back_button, menu_cd
incedent_cd = CallbackData("incedent", "action")

async def incedent_type_keyboard():
    keyboard = InlineKeyboardMarkup()
    seller_error_btn = InlineKeyboardButton("Ошибка моя / моей команды", callback_data=incedent_cd.new(action="seller_error"))
    manager_error_btn = InlineKeyboardButton("Ошибка менеджера", callback_data=incedent_cd.new(action="manager_error"))
    marketplace_error_btn = InlineKeyboardButton("Ошибка маркетплейса", callback_data=incedent_cd.new(action="marketplace_error"))
    keyboard.add(seller_error_btn)
    keyboard.add(manager_error_btn)
    keyboard.add(marketplace_error_btn)
    keyboard.add(back_button())
    return keyboard


async def incedent_work_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    seller_error_btn = InlineKeyboardButton("Поставки", callback_data=incedent_cd.new(action="incedent_shipment"))
    manager_error_btn = InlineKeyboardButton("Контент", callback_data=incedent_cd.new(action="incedent_content"))
    keyboard.add(seller_error_btn)
    keyboard.add(manager_error_btn)
    keyboard.add(back_button(action_name = back_action))
    return keyboard

async def incedent_shipment_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    driver_error_btn = InlineKeyboardButton("Заказать пропуск на водителя", callback_data=incedent_cd.new(action="incedent_shipment_driver"))
    documents_error_btn = InlineKeyboardButton("Отказ в приемке из-за неверных документов", callback_data=incedent_cd.new(action="incedent_shipment_documents"))
    remains_error_btn = InlineKeyboardButton("Неверные остатки", callback_data=incedent_cd.new(action="incedent_shipment_remains"))
    keyboard.add(driver_error_btn)
    keyboard.add(documents_error_btn)
    keyboard.add(remains_error_btn)
    keyboard.add(back_button(incedent_cd, back_action))
    return keyboard

async def incedent_content_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    content_infographic_btn = InlineKeyboardButton("Ошибка в инфографике", callback_data=incedent_cd.new(action="incedent_content_infographic"))
    content_text_btn = InlineKeyboardButton("Ошибка в тексте", callback_data=incedent_cd.new(action="incedent_content_text"))
    content_data_btn = InlineKeyboardButton("Ошибка в данных", callback_data=incedent_cd.new(action="incedent_content_data"))
    keyboard.add(content_infographic_btn)
    keyboard.add(content_text_btn)
    keyboard.add(content_data_btn)
    keyboard.add(back_button(incedent_cd, back_action))
    return keyboard

async def incedent_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=incedent_cd.new(action="incedent_continue_without_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(incedent_cd, back_action))
    return keyboard


async def incedent_confirm_keyboard():
    keyboard = InlineKeyboardMarkup()
    confirm_btn = InlineKeyboardButton("Подтвердить", callback_data=incedent_cd.new(action="incedent_confirm"))
    again_btn = InlineKeyboardButton("Заполнить заново", callback_data=menu_cd.new(action="back"))
    keyboard.add(confirm_btn)
    keyboard.add(again_btn)
    return keyboard

async def incedent_writed_kayboard():
    keyboard = InlineKeyboardMarkup()
    again_btn = InlineKeyboardButton("Вернуться в меню", callback_data=menu_cd.new(action="back"))
    keyboard.add(again_btn)
    return keyboard