from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def shipment_create_delivery_data_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    confirm_data_btn = InlineKeyboardButton("Подтверждение ранее согласованных данных", callback_data=task_cd.new(action="task_shipment_create_prev_data"))
    contact_btn = InlineKeyboardButton("Требует согласования", callback_data=task_cd.new(action="task_shipment_create_contact"))
    keyboard.add(confirm_data_btn)
    keyboard.add(contact_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def shipment_create_delivery_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_shipment_create_delivery_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard