from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button
from task_markups import task_cd

async def content_upload_image_task_type_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    change_btn = InlineKeyboardButton("Заменить текущие фото", callback_data=task_cd.new(action="task_content_upload_image_change"))
    new_btn = InlineKeyboardButton("Добавить новые фото", callback_data=task_cd.new(action="task_content_upload_image_new"))
    keyboard.add(change_btn)
    keyboard.add(new_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def content_upload_image_goods_info_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без добавления фото", callback_data=task_cd.new(action="task_content_upload_image_continue_no_photo"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def content_upload_image_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить", callback_data=task_cd.new(action="task_content_upload_image_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard