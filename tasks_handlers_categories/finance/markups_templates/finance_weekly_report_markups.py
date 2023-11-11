from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from markups import back_button
from task_markups import task_cd

async def finance_weekly_report_week_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления недели", callback_data=task_cd.new(action="task_finance_weekly_report_continue_without_week"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def finance_weekly_report_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_finance_weekly_report_continue_without_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard