#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.shipment.markups_templates.shipment_create_delivery_markups import *

from main import bot
from task_handlers import task_info

async def shipment_create_delivery_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Создать поставку"
    user_data[query.from_user.id] = {
        "current_message": "shipment_create_delivery_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await shipment_create_delivery_data_keyboard("task_delivery")
    user_data["prev_action"] = "create_delivery_shipment"

    await query.message.edit_text(text="Выберите данные для подтверждения поставки:", reply_markup=keyboard_markup)
    await query.answer()

#Получение склада
#Ожидание описания задачи
async def input_shipment_create_delivery_type_handler(query: CallbackQuery, user_data, warehouse_action, **kwargs):
    if (warehouse_action == "task_shipment_create_prev_data"):
        task_info["task_action"] = "Существующие данные"
    elif (warehouse_action == "task_shipment_create_contact"):
        task_info["task_action"] = "Требует согласования"
    else:
        task_info["task_action"] = "-"

    keyboard_markup = await shipment_create_delivery_description_keyboard(user_data["prev_action"])

    user_data[query.from_user.id] = {
        "current_message": "shipment_create_delivery_description",
        "last_bot_message_id": query.message.message_id
    }

    await query.message.edit_text(
        text="Склад записан.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_shipment_create_delivery_description_handler(message: types.Message, user_data, **kwargs):
    global task_info
    user_data[message.from_user.id] = { "current_message": "" }
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
        f"\n⚪️ Данные для подтверждения поставки: {task_info['task_action']}\n"
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
async def shipment_create_delivery_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    global task_info
    user_data[query.from_user.id] = { "current_message": "" }
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Данные для подтверждения поставки: {task_info['task_action']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )