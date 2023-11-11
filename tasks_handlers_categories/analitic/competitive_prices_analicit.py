#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery

from task_markups import *
from tasks_handlers_categories.analitic.markups_templates.competitive_prices_analicit_markups import *

from main import bot
from task_handlers import task_info

async def competitors_prices_links_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Анализ конкурентных цен"
    user_data[query.from_user.id] = {
        "current_message": "competitors_prices_links",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await competitors_prices_links_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "competitor_analysis"

    await query.message.edit_text(text="Перечислите ссылки на товары конкурентов через запятую", reply_markup=keyboard_markup)
    await query.answer()

#Получение ссылок на товары конкурентов
#Ождмание описания задачи
async def input_competitors_prices_links_handler(message: types.Message, user_data, **kwargs):
    task_info["competitors_links"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await competitors_prices_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Ссылки на товары конкурентов записаны.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "competitors_prices_analitic_description",
        "last_bot_message_id": sent_message.message_id
    }
#Если ссылки не ввели
#Ожидание описания задачи
async def input_competitors_prices_description_handler_without_links(query: CallbackQuery, user_data, **kwargs):
    task_info["competitors_links"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "competitors_prices_analitic_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await competitors_prices_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление ссылок на товары конкурентов.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )
#Получение описание задачи
#Ожидание подтверждения
async def input_competitors_prices_description_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Ссылки на конкурентов: {task_info['competitors_links']}\n"
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
async def competitors_prices_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Ссылки на конкурентов: {task_info['competitors_links']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )