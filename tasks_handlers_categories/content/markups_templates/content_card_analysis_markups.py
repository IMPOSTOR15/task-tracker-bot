from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def content_card_analysis_goods_ids_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без артикулов маркетплейса", callback_data=task_cd.new(action="task_content_card_analysis_continue_no_goods_ids"))
    all_btn = InlineKeyboardButton("Выбрать все арктикулы", callback_data=task_cd.new(action="task_content_card_analysis_continue_all_goods_ids"))
    keyboard.add(continue_btn)
    keyboard.add(all_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def content_card_analysis_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_content_card_analysis_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard