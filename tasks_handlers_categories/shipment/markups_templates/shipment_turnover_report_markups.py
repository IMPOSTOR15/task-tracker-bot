from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def shipment_turnover_report_date_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления периода", callback_data=task_cd.new(action="task_shipment_turnover_report_continue_no_date"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def shipment_turnover_report_goods_ids_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без артикулов маркетплейса", callback_data=task_cd.new(action="task_shipment_turnover_report_continue_no_goods_ids"))
    all_btn = InlineKeyboardButton("Выбрать все арктикулы", callback_data=task_cd.new(action="task_shipment_turnover_report_continue_all_goods_ids"))
    keyboard.add(continue_btn)
    keyboard.add(all_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def shipment_turnover_report_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_shipment_turnover_report_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard