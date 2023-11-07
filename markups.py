import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("menu", "action")

async def main_task_keyboard():
    keyboard = InlineKeyboardMarkup()
    incedent_btn = InlineKeyboardButton("Инцедент", callback_data=menu_cd.new(action="incedent"))
    task_btn = InlineKeyboardButton("Задача", callback_data=menu_cd.new(action="task"))
    keyboard.add(incedent_btn)
    keyboard.add(task_btn)
    return keyboard

def back_button(cd = menu_cd, action_name = "back"):
    return InlineKeyboardButton("Назад", callback_data=cd.new(action=action_name))