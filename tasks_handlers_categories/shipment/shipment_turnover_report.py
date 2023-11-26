#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.shipment.markups_templates.shipment_turnover_report_markups import *

from main import bot
from task_handlers import task_info

async def shipment_turnover_report_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["task_subcategory"] = "Отчет оборачиваемости"
    user_data[query.from_user.id] = {
        "current_message": "shipment_turnover_report_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await shipment_turnover_report_date_keyboard("task_delivery")
    user_data["prev_action"] = "turnover_report_shipment"

    await query.message.edit_text(text="Выберите дату начала периода отчета и Выберите дату конца периода отчета.\n Пример: 09.09.2023 - 18.09.2023", reply_markup=keyboard_markup)
    await query.answer()

#Получение даты анализа
#Ождмание айди товаров
async def input_shipment_turnover_report_date_handler(message: types.Message, user_data, **kwargs):
    task_info["task_date"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await shipment_turnover_report_goods_ids_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Даты периода записаны.\nУкажите артикулы маркетплейса через запятую",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "shipment_turnover_report_goods_ids",
        "last_bot_message_id": sent_message.message_id
    }

#Если дат не ввели
#Ождмание айди товаров
async def input_shipment_turnover_report_goods_ids_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    task_info["task_date"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "shipment_turnover_report_goods_ids",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await shipment_turnover_report_goods_ids_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление даты периода.\nУкажите артикулы маркетплейса через запятую",
        reply_markup=keyboard_markup
    )

#Получение айди товаров
#Ождмание описания задачи
async def input_shipment_turnover_report_description_handler(message: types.Message, user_data, **kwargs):
    task_info["goods_sku"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await shipment_turnover_report_description_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Артикулы маркетплейса записаны.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "shipment_turnover_report_description",
        "last_bot_message_id": sent_message.message_id
    }
#Если айди товаров выбраны все
#Ожидание описания задачи
async def input_shipment_turnover_report_description_handler_all_goods_ids(query: CallbackQuery, user_data, **kwargs):
    task_info["goods_sku"] = "Все"
    user_data[query.from_user.id] = {
        "current_message": "shipment_turnover_report_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await shipment_turnover_report_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="В отчёт войду все товары.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )

#Если айди товаров не ввели
#Ожидание описания задачи
async def input_shipment_turnover_report_description_handler_without_goods_ids(query: CallbackQuery, user_data, **kwargs):
    task_info["goods_sku"] = "-"
    user_data[query.from_user.id] = {
        "current_message": "shipment_turnover_report_description",
        "last_bot_message_id": query.message.message_id
    }

    keyboard_markup = await shipment_turnover_report_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Вы пропустили добавление артикулов маркетплейса.\nОпишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_shipment_turnover_report_confirmation_handler(message: types.Message, user_data, **kwargs):
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
        f"\n⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
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
async def shipment_turnover_report_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Период задачи: {task_info['task_date']}\n"
        f"\n⚪️ Выбранные артикулы: {task_info['goods_sku']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )