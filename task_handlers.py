from aiogram import types


from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from dbtools import get_sheet_name_by_chat_id, insert_task, mark_task_id_file
from google_sheets.google_sheets_tools import add_row_to_sheet

from task_markups import *
from main import SHEET_URL, bot

task_info = {}
task_group_text = """
Аналитика - группа задач связанная с проведением различных аналитических мероприятий.

Финансы - группа задач связанная с подготовкой и предоставлением отчетности для продавца.

Поставки - группа задач связанная с отчетностью и процессом поставок товаров на склады маркетплейса.

Контент - группа задач связанных с созданием, оформлением, изменением карточек товаров.

Обновить текстовый контент - задачи связанные с изменение текстового контента (название, описание, характеристики, SEO) в карточке товара.

"""
async def task_work_handler(query: CallbackQuery, user_data, **kwargs):
    keyboard_markup = await task_work_keyboard()
    await query.message.edit_text(text=f"{task_group_text}Выберите группу задачи", reply_markup=keyboard_markup)
    await query.answer()

async def task_analitic_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Аналитика"
    user_data["prev_action"] = "task_analitic"
    keyboard_markup = await task_analitic_keyboard()
    await query.message.edit_text(text="Группа задач связанная с проведением различных аналитических мероприятий.\n\nВыберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_finance_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Финансы"
    user_data["prev_action"] = "task_finance"
    keyboard_markup = await task_finance_keyboard()
    await query.message.edit_text(text="Группа задач связанная с подготовкой и предоставлением отчетности для продавца.\n\nВыберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_shipment_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Поставки"
    user_data["prev_action"] = "task_delivery"
    keyboard_markup = await task_shipment_keyboard()
    await query.message.edit_text(text="Группа задач связанная с отчетностью и процессом поставок товаров на склады маркетплейса.\n\nВыберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_content_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Контент"
    user_data["prev_action"] = "task_content"
    keyboard_markup = await task_content_keyboard()
    await query.message.edit_text(text="Группа задач связанных с созданием, оформлением, изменением карточек товаров.\n\nВыберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()

async def task_refresh_content_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_category"] = "Обновление контента"
    user_data["prev_action"] = "task_refresh_content"
    keyboard_markup = await task_refresh_content_keyboard()
    await query.message.edit_text(text="Задачи связанные с изменение текстового контента.\n\nВыберите подзадачу", reply_markup=keyboard_markup)
    await query.answer()


async def confirmed_task(query: CallbackQuery, user_data, **kwargs):
    keyboard_markup = await task_writed_kayboard()
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    task_info_defaults = {
        "task_category": "-",
        "task_subcategory": "-",
        "period_date": "-",
        "task_description": "-",
        "competitors_links": "-",
        "goods_sku": "-",
        "goods_info": "-",
        "task_action": "-",
        "add_by_user_id": user_id,
        "chat_id": chat_id,
        "task_date": "-",
        "task_report_week": "-",
        "warehouse":  "-",
    }

    task_info_data_to_db = {k: v for k, v in {**task_info_defaults, **task_info}.items() if k not in ['photo_paths', 'document_paths']}
    task_info_data = {k: v for k, v in {**task_info_defaults, **task_info}.items()}
    try:
        current_task_id = await insert_task(**task_info_data_to_db)
        if "photo_paths" in task_info:
            for photo_path in task_info["photo_paths"]:
                await mark_task_id_file(task_id = current_task_id, file_path = photo_path)

        if "document_paths" in task_info:
            for document_path in task_info["document_paths"]:
                await mark_task_id_file(task_id = current_task_id, file_path = document_path)
        # зАПИСЬ ЯЧЕЙКИ
        
        sheet_name = await get_sheet_name_by_chat_id(chat_id)
        add_row_to_sheet(SHEET_URL, sheet_name, task_info_data)

        await query.message.edit_text(
            text="Задача успешно добавлена",
            reply_markup=keyboard_markup
        )
    except Exception as e:
        await query.message.edit_text(
            text=f"Ошибка добавления задачи: \n{e.message}",
            reply_markup=keyboard_markup
        )
