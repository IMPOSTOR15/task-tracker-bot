from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def shipment_calculation_delivery_date_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    center_warehouse_btn = InlineKeyboardButton("Центральный", callback_data=task_cd.new(action="task_shipment_calculation_delivery_continue_center"))
    region_warehouse_btn = InlineKeyboardButton("Региональный", callback_data=task_cd.new(action="task_shipment_calculation_delivery_continue_region"))
    all_warehouse_btn = InlineKeyboardButton("Все", callback_data=task_cd.new(action="task_shipment_calculation_delivery_continue_all"))
    keyboard.add(center_warehouse_btn)
    keyboard.add(region_warehouse_btn)
    keyboard.add(all_warehouse_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def shipment_calculation_delivery_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_shipment_calculation_delivery_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard