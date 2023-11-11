from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from markups import back_button
from task_markups import task_cd

async def competitors_links_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления ссылок", callback_data=task_cd.new(action="task_competitors_analitic_continue_without_links"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def competitors_analitic_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_competitors_analitic_continue_without_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard