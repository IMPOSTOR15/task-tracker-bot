from aiogram import types


from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dbtools import get_sheet_name_by_chat_id, get_sheet_url_by_chat_id, insert_incedent
from google_sheets.google_sheets_tools import add_incedent_row_to_sheet

from incedent_markups import *
from main import bot

incedent_info = {}


incedent_type_text = """
Ошибка моя / моей команды. Инцидент произошел по вине продавца, представителя его команды или третьей стороны, привлеченной продавцом (например, ошибка в тексте инфографики, неверно сформированные отгрузочные документы).

Ошибка менеджера. Инцидент произошел по вине нашего или привлеченного нами специалиста.

Ошибка маркетплейса. Инцидент произошел по вине маркетплейса (например, технический сбой при приемке)

"""
incedent_works_text = """
Поставки - группа ошибок, связанная с поставками на склады МП, фулфилмент или логистикой.

Контент - группа ошибок, связанная с ошибками в карточках товара

Аналитика - группа задач связанная с проведением различных аналитических мероприятий

"""

class Form(StatesGroup):
    waiting_for_incident_description = State()

async def incedent_type_handler(query: CallbackQuery, user_data, **kwargs):
    keyboard_markup = await incedent_type_keyboard()
    await query.message.edit_text(text=f"{incedent_type_text}Выберите тип инцедента. По чьей вине произошел инцедент?", reply_markup=keyboard_markup)
    await query.answer()

async def seller_error_incedent_handler(query: CallbackQuery, user_data, action, **kwargs):
    if (action == "seller_error"):
        incedent_info['type'] = "Ошибка селлера"
        user_data["prev_action"] = "seller_error"
    if (action == "manager_error"):
        incedent_info['type'] = "Ошибка менеджера"
        user_data["prev_action"] = "manager_error"
    if (action == "marketplace_error"):
        incedent_info['type'] = "Ошибка маркетплейса"
        user_data["prev_action"] = "marketplace_error"

    user_data['current_error_state'] = user_data["prev_action"]
    keyboard_markup = await incedent_work_keyboard("incedent")
    await query.message.edit_text(text=f"{incedent_works_text}Выберите вид работ для инцедента", reply_markup=keyboard_markup)
    await query.answer()

async def shipment_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['work_category'] = "Поставки"
    print(user_data["prev_action"])

    keyboard_markup = await incedent_shipment_keyboard(user_data['current_error_state'])
    user_data["prev_action"] = "incedent_shipment"
    await query.message.edit_text(text="Выберите вид работ для инцедента c поставкой", reply_markup=keyboard_markup)
    await query.answer()

async def content_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['work_category'] = "Контент"
    keyboard_markup = await incedent_content_keyboard(user_data['current_error_state'])
    user_data["prev_action"] = "incedent_content"
    await query.message.edit_text(text="Выберите вид работ для инцедента с контентом", reply_markup=keyboard_markup)
    await query.answer()

async def description_incedent_handler(query: CallbackQuery, user_data, action, **kwargs):
    user_data[query.from_user.id] = {
        "current_message": "description_incedent",
        "last_bot_message_id": query.message.message_id  # Сохраняем message_id последнего сообщения бота
    }

    keyboard_markup = await incedent_description_keyboard(user_data["prev_action"])
    if (action == "incedent_content_infographic" or action == "incedent_content_text" or action == "incedent_content_data"):
        user_data["prev_action"] = 'incedent_content'
        msg_text = "Опишите инцедент подробнее, если это требуется. Также прикрепите sku или ссылку на карточку товара\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи."
    if (action == "incedent_shipment_remains" or action == "incedent_shipment_documents" or action == "incedent_shipment_driver"):
        user_data["prev_action"] = 'incedent_shipment'
        msg_text = "Опишите инцедент подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи."

    await query.message.edit_text(text=msg_text, reply_markup=keyboard_markup)
    await query.answer()


async def description_incedent_input(message: types.Message, user_data, **kwargs):
    incedent_info["incedent_description"] = message.text

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]
    
    print(incedent_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Тип инцидента: {incedent_info['type']}\n"
        f"\n⚪️ Категория работы: {incedent_info['work_category']}\n"
        f"\n⚪️ Описание инцидента: {incedent_info['incedent_description']}"
    )

    keyboard_markup = await incedent_confirm_keyboard()
    await bot.send_message(
        chat_id=message.chat.id,
        text=confirmation_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard_markup
    )

async def description_incedent_input_without_description(query: CallbackQuery, user_data, **kwargs):
    incedent_info["incedent_description"] = ''
    
    print(incedent_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Тип инцидента: {incedent_info['type']}\n"
        f"\n⚪️ Категория работы: {incedent_info['work_category']}\n"
        f"\n⚪️ Описание инцидента: {incedent_info['incedent_description']}"
    )
    keyboard_markup = await incedent_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )

async def confirmed_incedent(query: CallbackQuery, user_data, **kwargs):
    chat_id = query.message.chat.id
    # Добавить логику по добавлению инцедента в бд и отправки уведомления и гугл таблица тоже
    await insert_incedent(**incedent_info)
    print(incedent_info)
    sheet_name = await get_sheet_name_by_chat_id(chat_id)
    sheet_url = await get_sheet_url_by_chat_id(chat_id)
    add_incedent_row_to_sheet(sheet_url, sheet_name, incedent_info)
    keyboard_markup = await incedent_writed_kayboard()
    await query.message.edit_text(
        text="Инцедент успешно добавлен",
        reply_markup=keyboard_markup
    )
