from aiogram import types


from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from incedent_markups import *
from main import bot

incedent_info = {}

class Form(StatesGroup):
    waiting_for_incident_description = State()

async def incedent_type_handler(query: CallbackQuery, user_data, **kwargs):
    keyboard_markup = await incedent_type_keyboard()
    await query.message.edit_text(text="Выберите тип инцедента. По чьей вине произошел инцедент?", reply_markup=keyboard_markup)
    await query.answer()

async def seller_error_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['type'] = "Ошибка селлера"
    user_data["prev_action"] = "seller_error"
    keyboard_markup = await incedent_work_keyboard("incedent")
    await query.message.edit_text(text="Выберите вид работ для инцедента", reply_markup=keyboard_markup)
    await query.answer()


async def manager_error_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['type'] = "Ошибка менеджера"
    user_data["prev_action"] = "manager_error"
    keyboard_markup = await incedent_work_keyboard("incedent")
    await query.message.edit_text(text="Выберите вид работ для инцедента", reply_markup=keyboard_markup)
    await query.answer()

async def marketplace_error_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['type'] = "Ошибка маркетплейса"
    user_data["prev_action"] = "marketplace_error"
    keyboard_markup = await incedent_work_keyboard("incedent")
    await query.message.edit_text(text="Выберите вид работ для инцедента", reply_markup=keyboard_markup)
    await query.answer()

async def shipment_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['work_category'] = "Поставки"
    keyboard_markup = await incedent_shipment_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "incedent_shipment"
    await query.message.edit_text(text="Выберите вид работ для инцедента c поставкой", reply_markup=keyboard_markup)
    await query.answer()

async def content_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    incedent_info['work_category'] = "Контент"
    keyboard_markup = await incedent_content_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "incedent_content"
    await query.message.edit_text(text="Выберите вид работ для инцедента с контентом", reply_markup=keyboard_markup)
    await query.answer()

async def description_incedent_handler(query: CallbackQuery, user_data, **kwargs):
    user_data[query.from_user.id] = {
        "current_message": "description_incedent",
        "last_bot_message_id": query.message.message_id  # Сохраняем message_id последнего сообщения бота
    }

    keyboard_markup = await incedent_description_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "description_incedent"
    user_data["current_message"] = "description_incedent"
    await query.message.edit_text(text="Опишите инцедент подробнее, если это требуется", reply_markup=keyboard_markup)
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
        f"⚪️ Тип инцидента: {incedent_info['type']}\n"
        f"⚪️ Категория работы: {incedent_info['work_category']}\n"
        f"⚪️ Описание инцидента: {incedent_info['incedent_description']}"
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
        f"⚪️ Тип инцидента: {incedent_info['type']}\n"
        f"⚪️ Категория работы: {incedent_info['work_category']}\n"
        f"⚪️ Описание инцидента: -"
    )
    keyboard_markup = await incedent_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )

async def confirmed_incedent(query: CallbackQuery, user_data, **kwargs):

    # Добавить логику по добавлению инцедента в бд и отправки уведомления и гугл таблица тоже

    keyboard_markup = await incedent_writed_kayboard()
    await query.message.edit_text(
        text="Инцедент успешно добавлен",
        reply_markup=keyboard_markup
    )
