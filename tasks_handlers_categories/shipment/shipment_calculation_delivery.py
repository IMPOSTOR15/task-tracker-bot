#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.shipment.markups_templates.shipment_calculation_delivery_markups import *

from main import bot
from task_handlers import task_info

async def shipment_calculation_delivery_warehouse_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Отчет по остаткам с разбивкой по складам"
    user_data[query.from_user.id] = {
        "current_message": "shipment_calculation_delivery_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await shipment_calculation_delivery_date_keyboard("task_delivery")
    user_data["prev_action"] = "calculation_delivery_shipment"

    await query.message.edit_text(text="Выберите склад для расчета поставки из списка:", reply_markup=keyboard_markup)
    await query.answer()

#Получение склада
#Ожидание описания задачи
async def input_shipment_calculation_delivery_warehouse_handler(query: CallbackQuery, user_data, warehouse_action, **kwargs):
    if (warehouse_action == "task_shipment_calculation_delivery_continue_center"):
        task_info["warehouse"] = "Центральный"
    elif (warehouse_action == "task_shipment_calculation_delivery_continue_region"):
        task_info["warehouse"] = "Региональный"
    elif (warehouse_action == "task_shipment_calculation_delivery_continue_all"):
        task_info["warehouse"] = "Все"
    else:
        task_info["warehouse"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "shipment_calculation_delivery_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await shipment_calculation_delivery_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Склад записан.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_shipment_calculation_delivery_description_handler(message: types.Message, user_data, **kwargs):
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
        f"\n⚪️ Склад поставки: {task_info['warehouse']}\n"
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
async def shipment_calculation_delivery_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    global task_info
    user_data[query.from_user.id] = { "current_message": "" }
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Склад поставки: {task_info['warehouse']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )