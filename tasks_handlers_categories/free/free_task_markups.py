from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd
from markups import menu_cd
async def free_task_info_start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(back_button(menu_cd, "task"))
    return keyboard

async def free_task_info_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить", callback_data=task_cd.new(action="free_task_continue"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard