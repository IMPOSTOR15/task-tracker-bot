from aiogram import types


from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from task_markups import *
from main import bot

task_info = {}

async def task_work_handler(query: CallbackQuery, user_data, **kwargs):
    keyboard_markup = await task_work_keyboard()
    await query.message.edit_text(text="Выберите группу задачи", reply_markup=keyboard_markup)
    await query.answer()

async def task_analitic_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Аналитика"
    user_data["prev_action"] = "task_analitic"
    keyboard_markup = await task_analitic_keyboard()
    await query.message.edit_text(text="Группа задач связанная с проведением различных аналитических мероприятий. \n Выберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_finance_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Финансы"
    user_data["prev_action"] = "task_finance"
    keyboard_markup = await task_finance_keyboard()
    await query.message.edit_text(text="Группа задач связанная с подготовкой и предоставлением отчетности для продавца. \n Выберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_shipment_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Поставки"
    user_data["prev_action"] = "task_delivery"
    keyboard_markup = await task_shipment_keyboard()
    await query.message.edit_text(text="Группа задач связанная с отчетностью и процессом поставок товаров на склады маркетплейса. \n Выберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_content_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Контент"
    user_data["prev_action"] = "task_content"
    keyboard_markup = await task_content_keyboard()
    await query.message.edit_text(text="Группа задач связанных с созданием, оформлением, изменением карточек товаров. \n Выберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_refresh_content_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Обновление контента"
    user_data["prev_action"] = "task_refresh_content"
    keyboard_markup = await task_refresh_content_keyboard()
    await query.message.edit_text(text="Задачи связанные с изменение текстового контента. \n Выберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()


async def confirmed_task(query: CallbackQuery, user_data, **kwargs):
    # Добавить логику по добавлению задачи в бд и отправки уведомления и гугл таблица тоже
    keyboard_markup = await task_writed_kayboard()
    await query.message.edit_text(
        text="Задача успешно добавлена",
        reply_markup=keyboard_markup
    )