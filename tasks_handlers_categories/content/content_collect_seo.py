#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.content.markups_templates.content_collect_seo_markups import *

from main import bot
from task_handlers import task_info

async def content_collect_seo_skus_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Собрать SEO"
    user_data[query.from_user.id] = {
        "current_message": "content_collect_seo_goods_ids",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await content_collect_seo_goods_ids_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "collect_seo_content"
    await query.answer()
    await query.message.edit_text(
        text="Укажите артикулы карточек маркетплейса для сбора даных через запятую",
        reply_markup=keyboard_markup
    )
    

#Получение айди товаров
#Ождмание описания задачи
async def input_content_collect_seo_description_handler(message: types.Message, user_data, **kwargs):
    task_info["goods_sku"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await content_collect_seo_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Артикулы маркетплейса записаны.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "content_collect_seo_description",
        "last_bot_message_id": sent_message.message_id
    }

#Если айди товаров не ввели
#Ожидание описания задачи
async def input_content_collect_seo_description_handler_without_goods_ids(query: CallbackQuery, user_data, **kwargs):
    task_info["goods_sku"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "content_collect_seo_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await content_collect_seo_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление артикулов маркетплейса.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_content_collect_seo_confirmation_handler(message: types.Message, user_data, **kwargs):
    global task_info
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]
        
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await bot.send_message(
        chat_id=message.chat.id,
        text=confirmation_message,
        reply_markup=keyboard_markup
    )

#Если описание не ввели
#Ожидание подтверждения
async def content_collect_seo_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    global task_info
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )