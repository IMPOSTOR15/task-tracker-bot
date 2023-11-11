#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery

from task_markups import *
from tasks_handlers_categories.finance.markups_templates.finance_price_elasticity_markups import *

from main import bot
from task_handlers import task_info

async def finance_price_elasticity_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Эластичность цены"
    user_data[query.from_user.id] = {
        "current_message": "finance_price_elasticity_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await finance_price_elasticity_date_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "price_elasticity_financial"

    await query.message.edit_text(text="Выберите дату начала периода отчета и Выберите дату конца периода отчета.\n Пример: 09.09.2023 - 18.09.2023", reply_markup=keyboard_markup)
    await query.answer()

#Получение даты анализа
#Ождмание описания задачи
async def input_finance_price_elasticity_date_handler(message: types.Message, user_data, **kwargs):
    task_info["task_date"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await finance_price_elasticity_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Даты периода записаны.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "finance_price_elasticity_description",
        "last_bot_message_id": sent_message.message_id
    }

#Если дат не ввели
#Ожидание описания задачи
async def input_finance_price_elasticity_description_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    task_info["task_date"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "finance_price_elasticity_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await finance_price_elasticity_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление даты периода.\nОпишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_finance_price_elasticity_description_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Период задачи: {task_info['task_date']}\n"
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
async def finance_price_elasticity_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Период задачи: {task_info['task_date']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )