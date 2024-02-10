#Ожидание ссылок на конкурентов
from aiogram import types

from aiogram.types import CallbackQuery
from hellpers import clean_task_info

from task_markups import *
from tasks_handlers_categories.free.free_task_markups import *
from save_tools import process_media

from main import bot
from task_handlers import task_info

#Получение информации о товарах
#Ождмание описания задачи
async def free_task_date_handler(query: CallbackQuery, user_data, **kwargs):
    task_info["photo_paths"] = []
    task_info["document_paths"] = []
    
    task_info["task_subcategory"] = "Свободная задача"
    user_data[query.from_user.id] = {
        "current_message": "free_task_date",
        "last_bot_message_id": query.message.message_id
    }
    keyboard_markup = await free_task_info_start_keyboard()
    user_data["prev_action"] = "task_free"
    
    await query.message.edit_text(
        text="""Свободная задача\n\nОпишите, что необходимо сделать""",
        reply_markup=keyboard_markup,
        parse_mode='Markdown',
    )
    await query.answer()

async def input_free_task_date_handler(message: types.Message, user_data, **kwargs):
    global task_info
    is_last_in_album = False

    if message.text:
        if (task_info.get("task_description")):
            task_info["task_description"] = task_info["task_description"] + '\n' + message.text
        else:
            task_info["task_description"] = message.text
    
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
    
        keyboard_markup = await free_task_info_keyboard(user_data["prev_action"])
        sent_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Данные записаны.\nДобавьте другие файлы и/или информацию при необходимости \n\n⚠Отправляйте не более 10 файлов за раз⚠",
            reply_markup=keyboard_markup
        )

        user_data[message.from_user.id] = {
            "current_message": "free_task_date",
            "last_bot_message_id": sent_message.message_id
        }

#Если дат не ввели
#Ожидание описания задачи
async def input_free_task_description_handler_without_date(query: CallbackQuery, user_data, **kwargs):
    global task_info
    user_data[query.from_user.id] = { "current_message": "" }

    if 'photo_paths' not in task_info:
        task_info['photo_paths'] = []
    if 'document_paths' not in task_info:
        task_info['document_paths'] = []
    
    if "last_bot_message_id" in user_data[query.from_user.id]:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=user_data[query.from_user.id]["last_bot_message_id"])
        del user_data[query.from_user.id]["last_bot_message_id"]
    
    task_info = clean_task_info(task_info)
    confirmation_message = (
        "Пожалуйста, удостоверьтесь в правильности собранных данных:\n"
        f"\n⚪️ Подкатегория задачи: {task_info['task_subcategory']}\n"
        f"\n⚪️ Описание задачи: {task_info['task_description']}\n"
        f"\n⚪️ Фото: {task_info['photo_paths']}\n"
        f"\n⚪️ Документы: {task_info['document_paths']}\n"
    )

    keyboard_markup = await task_confirm_keyboard()
    await query.message.edit_text(
        text=confirmation_message,
        reply_markup=keyboard_markup
    )
