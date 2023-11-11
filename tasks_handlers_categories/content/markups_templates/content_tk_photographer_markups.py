from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def content_tk_photographer_goods_info_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления информации о товарах", callback_data=task_cd.new(action="task_content_tk_photographer_continue_no_date"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def content_tk_photographer_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_content_tk_photographer_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard