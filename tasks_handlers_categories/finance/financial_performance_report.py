#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.finance.markups_templates.financial_performance_report_markups import *

from main import bot
from task_handlers import task_info

report_description_text = """
В отчете отражается влияние проведенных за период изменений (например, повышение цены) на финансовые показатели (например, маржинальная выручка за период).
"""
async def financial_performance_report_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Отчет о проделанной работе в разрезе финансовых показателей"
    user_data[query.from_user.id] = {
        "current_message": "financial_performance_report_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await financial_performance_report_date_keyboard("task_finance")
    user_data["prev_action"] = "report_section_financial"

    await query.message.edit_text(text=f"{report_description_text}\nВыберите дату начала периода отчета и Выберите дату конца периода отчета.\n Пример: 09.09.2023 - 18.09.2023", reply_markup=keyboard_markup)
    await query.answer()

#Получение даты анализа
#Ождмание описания задачи
async def input_financial_performance_report_date_handler(message: types.Message, user_data, **kwargs):
    task_info["task_date"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await financial_performance_report_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Даты периода записаны.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "financial_performance_report_description",
        "last_bot_message_id": sent_message.message_id
    }

#Если дат не ввели
#Ожидание описания задачи
async def input_financial_performance_report_description_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    task_info["task_date"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "financial_performance_report_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await financial_performance_report_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление даты периода.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_financial_performance_report_description_handler(message: types.Message, user_data, **kwargs):
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
        f"\n⚪️ Период задачи: {task_info['task_date']}\n"
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
async def financial_performance_report_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    global task_info
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Период задачи: {task_info['task_date']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )