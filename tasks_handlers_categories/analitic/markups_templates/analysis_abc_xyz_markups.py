from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from markups import back_button
from task_markups import task_cd

async def analysis_abc_xyz_date_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления периода", callback_data=task_cd.new(action="task_analysis_abc_xyz_continue_without_date"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def analysis_abc_xyz_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_analysis_abc_xyz_continue_without_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard