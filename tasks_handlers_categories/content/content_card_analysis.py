#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery

from task_markups import *
from tasks_handlers_categories.content.markups_templates.content_card_analysis_markups import *

from main import bot
from task_handlers import task_info

async def content_card_analysis_skus_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Анализ карточки"
    user_data[query.from_user.id] = {
        "current_message": "content_card_analysis_goods_ids",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await content_card_analysis_goods_ids_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "card_analysis_content"
    await query.answer()
    await query.message.edit_text(
        text="Укажите артикулы карточек маркетплейса для анализа через запятую",
        reply_markup=keyboard_markup
    )
    

#Получение айди товаров
#Ождмание описания задачи
async def input_content_card_analysis_description_handler(message: types.Message, user_data, **kwargs):
    task_info["goods_sku"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await content_card_analysis_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Артикулы маркетплейса записаны.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "content_card_analysis_description",
        "last_bot_message_id": sent_message.message_id
    }
#Если айди товаров выбраны все
#Ожидание описания задачи
async def input_content_card_analysis_description_handler_all_goods_ids(query: CallbackQuery, user_data, **kwargs):
    task_info["goods_sku"] = "Все"
    user_data[query.from_user.id] = {
        "current_message": "content_card_analysis_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await content_card_analysis_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="В отчёт войду все товары.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Если айди товаров не ввели
#Ожидание описания задачи
async def input_content_card_analysis_description_handler_without_goods_ids(query: CallbackQuery, user_data, **kwargs):
    task_info["goods_sku"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "content_card_analysis_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await content_card_analysis_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление артикулов маркетплейса.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_content_card_analysis_confirmation_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await bot.send_message(
        chat_id=message.chat.id,
        text=confirmation_message,
        reply_markup=keyboard_markup
    )

#Если описание не ввели
#Ожидание подтверждения
async def content_card_analysis_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )