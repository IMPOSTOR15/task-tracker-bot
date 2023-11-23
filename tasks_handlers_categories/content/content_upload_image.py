#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from save_tools import process_media

from task_markups import *
from tasks_handlers_categories.content.markups_templates.content_upload_image_markups import *

from main import bot
from task_handlers import task_info

async def content_upload_image_action_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["photo_paths"] = []
    
    task_info["task_subcategory"] = "Загрузка фото"
    user_data[query.from_user.id] = {
        "current_message": "content_upload_image_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await content_upload_image_task_type_keyboard(user_data["prev_action"])
    user_data["prev_action"] = "new_image_content"
    
    await query.message.edit_text(text="Выберите действие",
    reply_markup=keyboard_markup
    )
    await query.answer()


#Обработка подтипа
#Ожидание файлов фото
async def input_content_upload_image_task_type_handler(query: CallbackQuery, user_data, action, **kwargs):
    if (action == 'task_content_upload_image_change'):
        task_info["task_action"] = "Изменить фото"
    if (action == 'task_content_upload_image_new'):
        task_info["task_action"] = "Новое фото"

    user_data[query.from_user.id] = {
        "current_message": "content_upload_image_file",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await content_upload_image_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Отправьте новое фото или прекрепите ссылку на файловое хранилище (удостоверьтесь что доступ к фото открыт)",
        reply_markup=keyboard_markup
    )

async def input_content_upload_image_date_handler(message: types.Message, user_data, **kwargs):
    global task_info
    is_last_in_album = False

    if message.text:
        task_info["goods_info"] = message.text
    else:
        task_info["goods_info"] = '-'
    
    # Обработка медиа в сообщении
    task_info = await process_media(message, task_info)

    if not message.media_group_id or message.media_group_id != user_data.get("last_media_group_id", None):
        is_last_in_album = True
        user_data["last_media_group_id"] = message.media_group_id

    if is_last_in_album:
        if "last_bot_message_id" in user_data[message.from_user.id]:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
            del user_data[message.from_user.id]["last_bot_message_id"]
    
        keyboard_markup = await content_upload_image_goods_info_keyboard(user_data["prev_action"])
        sent_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Данные записаны.\nДобавьте другие файлы и/или информацию при необходимости",
            reply_markup=keyboard_markup
        )
        user_data[message.from_user.id] = {
            "current_message": "content_upload_image_file",
            "last_bot_message_id": sent_message.message_id
        }
#Если дат не ввели
#Ожидание описания задачи
async def input_content_upload_image_description_handler_without_data(query: CallbackQuery, user_data, **kwargs):
    if 'photo_paths' not in task_info:
        task_info['photo_paths'] = []
    if 'document_paths' not in task_info:
        task_info['document_paths'] = []

    user_data[query.from_user.id] = {
        "current_message": "content_upload_image_description",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await content_upload_image_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Опишите задачу подробнее, если это требуется",
        reply_markup=keyboard_markup
    )

#Получение описание задачи
#Ожидание подтверждения
async def input_content_upload_image_confirmation_handler(message: types.Message, user_data, **kwargs):
    task_info["task_description"] = message.text
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    if "last_bot_message_id" in user_data[message.from_user.id]:
        await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
        del user_data[message.from_user.id]["last_bot_message_id"]

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Тип задачи: {task_info['task_action']}\n"
        f"\n⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"\n⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"\n⚪️ Документы: {task_info['document_paths']}\n"
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
async def content_upload_image_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    task_info["task_description"] = "-"

    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Тип задачи: {task_info['task_action']}\n"
        f"\n⚪️ Ссылки на товары: {task_info['goods_info']}\n"
        f"\n⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"\n⚪️ Документы: {task_info['document_paths']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )