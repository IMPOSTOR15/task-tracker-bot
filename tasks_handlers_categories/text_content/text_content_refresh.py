#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from save_tools import process_media

from task_markups import *
from tasks_handlers_categories.text_content.markups_templates.text_content_refresh_markups import *

from main import bot
from task_handlers import task_info

async def text_content_refresh_sku_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["photo_paths"] = []
    
    task_info["task_category"] = "Обновление контента"
    user_data[query.from_user.id] = {
        "current_message": "text_content_refresh_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await text_content_refresh_task_sku_keyboard('task')
    user_data["prev_action"] = "task"
    
    await query.message.edit_text(text="Укажите артикул товара или ссылку на него",
    reply_markup=keyboard_markup
    )
    await query.answer()

async def input_text_content_refresh_type_handler(message: types.Message, user_data, **kwargs):
    global task_info
    if message.text:
        task_info["goods_info"] = message.text
    else:
        task_info["goods_info"] = '-'

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await text_content_refresh_task_type_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите, куда необходимо внести изменения",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "text_content_refresh_type",
        "last_bot_message_id": sent_message.message_id
    }
#Обработка подтипа
#Ожидание файлов фото
async def input_text_content_refresh_task_type_handler(query: CallbackQuery, user_data, action, **kwargs):
    if (action == 'task_content_refresh_product_name'):
        task_info["task_action"] = "Изменить название"
    elif (action == 'task_content_refresh_product_description'):
        task_info["task_action"] = "Изменить описание"
    elif (action == 'task_content_refresh_product_charact'):
        task_info["task_action"] = "Изменить характеристики"
    elif (action == 'task_content_refresh_products_seo'):
        task_info["task_action"] = "Изменить SEO"
    else:
        task_info["task_action"] = "-"

    user_data[query.from_user.id] = {
        "current_message": "text_content_refresh_file",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await text_content_refresh_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Отправьте новое фото или прекрепите ссылку на файловое хранилище (удостоверьтесь что доступ к фото открыт)",
        reply_markup=keyboard_markup
    )

async def input_text_content_refresh_file_handler(message: types.Message, user_data, **kwargs):
    global task_info
    if message.text:
        task_info["goods_info"] = message.text
    else:
        task_info["goods_info"] = '-'

    #Обработка медиа в сообщении
    task_info = await process_media(message, task_info)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    keyboard_markup = await text_content_refresh_goods_info_keyboard(user_data["prev_action"])
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Данные записаны.\nДобавьте другие файлы и/или информацию при необходимости",
        reply_markup=keyboard_markup
    )
    user_data[message.from_user.id] = {
        "current_message": "text_content_refresh_file",
        "last_bot_message_id": sent_message.message_id
    }

#Если дат не ввели
#Ожидание описания задачи
async def input_text_content_refresh_description_handler_without_data(query: CallbackQuery, user_data, **kwargs):
    if 'photo_paths' not in task_info:
        task_info['photo_paths'] = ["-"]
    if 'document_path' not in task_info:
        task_info['document_path'] = ["-"]

    user_data[query.from_user.id] = {
        "current_message": "text_content_refresh_description",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await text_content_refresh_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Опишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_text_content_refresh_confirmation_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Тип задачи: {task_info['task_action']}\n"
        f"⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"⚪️ Документы: {task_info['document_path']}\n"
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
async def text_content_refresh_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"⚪️ Категория задачи: {task_info['task_category']}\n"
        f"⚪️ Тип задачи: {task_info['task_action']}\n"
        f"⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"⚪️ Документы: {task_info['document_path']}\n"
        f"⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )
    print(task_info)