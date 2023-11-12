#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from save_tools import process_media

from task_markups import *
from tasks_handlers_categories.content.markups_templates.content_creating_infographics_markups import *

from main import bot
from task_handlers import task_info

async def content_creating_infographics_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["photo_paths"] = []
    task_info['document_paths'] = []
    
    task_info["task_subcategory"] = "Создание инфографики"
    user_data[query.from_user.id] = {
        "current_message": "content_creating_infographics_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await content_creating_infographics_goods_info_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "infographics_content"
    
    await query.message.edit_text(text="""Укажите ссылки на исходники через запятую или отправьте файлы\n(используется если контент предоставляется продавцом)\nУкажите артикул ваш или маркетплейса через запятую\n(используется если ТЗ для дизайнера создаем мы)\n(удостоверьтесь, что к ним открыт доступ)\n⚠Отправляйте не более 10 файлов за раз⚠""",
    reply_markup=keyboard_markup
    )
    await query.answer()

async def input_content_creating_infographics_date_handler(message: types.Message, user_data, **kwargs):
    global task_info
    if message.text:
        task_info["goods_info"] = message.text
    else:
        task_info["goods_info"] = '-'
    #Обработка медиа в сообщении
    task_info = await process_media(message, task_info)

    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await content_creating_infographics_goods_info_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Данные записаны.\nДобавьте другие файлы и/или информацию при необходимости",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "content_creating_infographics_date",
        "last_bot_message_id": sent_message.message_id
    }

#Если дат не ввели
#Ожидание описания задачи
async def input_content_creating_infographics_description_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    if 'photo_paths' not in task_info:
        task_info['photo_paths'] = []
    if 'document_paths' not in task_info:
        task_info['document_paths'] = []

    user_data[query.from_user.id] = {
        "current_message": "content_creating_infographics_description",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await content_creating_infographics_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Опишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_content_creating_infographics_description_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"⚪️ Документы: {task_info['document_paths']}\n"
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
async def content_creating_infographics_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"⚪️ Документы: {task_info['document_paths']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )
    print(task_info)