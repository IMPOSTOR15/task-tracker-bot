#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.content.markups_templates.content_tk_photographer_markups import *
from save_tools import process_media

from main import bot
from task_handlers import task_info



#Получение информации о товарах
#Ождмание описания задачи
async def content_tk_photographer_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["photo_paths"] = []
    
    task_info["task_subcategory"] = "ТЗ для фотографаы"
    user_data[query.from_user.id] = {
        "current_message": "content_tk_photographer_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await content_tk_photographer_goods_info_keyboard("task_content")
    user_data["prev_action"] = "tk_photographer_content"
    
    await query.message.edit_text(text="""Укажите артикул товара на маркетплейсе через запятую или ссылки на исходники товара или референс конкурента через запятую \nТакже можно прикрепить фото, файлы или ссылки на изображения (удостоверьтесь, что к ним открыт доступ)\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.\n\n⚠Отправляйте не более 10 файлов за раз⚠""",
    reply_markup=keyboard_markup
    )
    await query.answer()

async def input_content_tk_photographer_date_handler(message: types.Message, user_data, **kwargs):
    global task_info
    is_last_in_album = False

    if message.text:
        task_info["goods_info"] = message.text
    else:
        task_info["goods_info"] = '-'
    
    # Обработка медиа в сообщении
    task_info = await process_media(message, task_info)

    # Check if the message is the last in its album
    if not message.media_group_id or message.media_group_id != user_data.get("last_media_group_id", None):
        is_last_in_album = True
        user_data["last_media_group_id"] = message.media_group_id


    if is_last_in_album:

        if "last_bot_message_id" in user_data[message.from_user.id]:
            await bot.delete_message(chat_id=message.chat.id, message_id=user_data[message.from_user.id]["last_bot_message_id"])
            del user_data[message.from_user.id]["last_bot_message_id"]
    
        keyboard_markup = await content_tk_photographer_goods_info_keyboard(user_data["prev_action"])
        sent_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Данные записаны.\nДобавьте другие файлы и/или информацию при необходимости \n\n⚠Отправляйте не более 10 файлов за раз⚠",
            reply_markup=keyboard_markup
        )
        user_data[message.from_user.id] = {
            "current_message": "content_tk_photographer_date",
            "last_bot_message_id": sent_message.message_id
        }

#Если дат не ввели
#Ожидание описания задачи
async def input_content_tk_photographer_description_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    if 'photo_paths' not in task_info:
        task_info['photo_paths'] = []
    if 'document_paths' not in task_info:
        task_info['document_paths'] = []
    user_data[query.from_user.id] = {
        "current_message": "content_tk_photographer_description",
        "last_bot_message_id": query.message.message_id
    }
    
    keyboard_markup = await content_tk_photographer_description_keyboard(user_data["prev_action"])
    await query.message.edit_text(
        text="Опишите задачу подробнее, если это требуется\n\n⚠Не забудьте отправить текст прежде чем перейти к следующему шагу⚠\n\nИначе необходимое текстовое сопровождение не добавиться к задачи.",
        reply_markup=keyboard_markup
    )
#Получение описание задачи
#Ожидание подтверждения
async def input_content_tk_photographer_description_handler(message: types.Message, user_data, **kwargs):
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
        f"\n⚪️ Данные о товарах: {task_info['goods_info']}\n"
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
async def content_tk_photographer_confirmation_handler_without_description(query: CallbackQuery, user_data, **kwargs):
    global task_info
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Категория задачи: {task_info['task_category']}\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Данные о товарах: {task_info['goods_info']}\n"
        f"\n⚪️ Фото товаров: {task_info['photo_paths']}\n"
        f"\n⚪️ Документы: {task_info['document_paths']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}"
    )
    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )