from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def financial_performance_report_date_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления периода", callback_data=task_cd.new(action="task_financial_performance_report_continue_no_date"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def financial_performance_report_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_financial_performance_report_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard