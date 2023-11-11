from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from markups import back_button, menu_cd
from task_markups import task_cd

async def text_content_refresh_task_sku_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(back_button(menu_cd, back_action))
    return keyboard

async def text_content_refresh_task_type_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    name_btn = InlineKeyboardButton("Название", callback_data=task_cd.new(action="task_content_refresh_product_name"))
    desc_btn = InlineKeyboardButton("Описание", callback_data=task_cd.new(action="task_content_refresh_product_description"))
    charact_btn = InlineKeyboardButton("Характеристики", callback_data=task_cd.new(action="task_content_refresh_product_charact"))
    seo_btn = InlineKeyboardButton("SEO", callback_data=task_cd.new(action="task_content_refresh_products_seo"))
    keyboard.add(name_btn)
    keyboard.add(desc_btn)
    keyboard.add(charact_btn)
    keyboard.add(seo_btn)
    keyboard.add(back_button(menu_cd, back_action))
    return keyboard

async def text_content_refresh_goods_info_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить", callback_data=task_cd.new(action="task_content_refresh_continue_no_data"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard

async def text_content_refresh_description_keyboard(back_action):
    keyboard = InlineKeyboardMarkup()
    continue_btn = InlineKeyboardButton("Продолжить без описания", callback_data=task_cd.new(action="task_content_refresh_continue_no_description"))
    keyboard.add(continue_btn)
    keyboard.add(back_button(task_cd, back_action))
    return keyboard