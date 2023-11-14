import os
from aiogram import types
from dbtools import insert_file_document, insert_file_photo
from main import bot, SAVE_PATH
import secrets

async def process_media(message: types.Message, task_info):
    """
    Обработка медиафайлов в сообщении.

    :param message: Объект сообщения, содержащего медиа.
    :param task_info: Словарь данных пользователя для сохранения путей к файлам.
    :return: Обновленный task_info с путями к фото и документам.
    """
    print('process media')
    if message.photo:
        highest_resolution_photo = message.photo[-1]
        photo_path = await save_file(highest_resolution_photo.file_id, message.from_user.id)
        await insert_file_photo(file_path = photo_path)
        if "photo_paths" not in task_info:
            task_info["photo_paths"] = []
        task_info["photo_paths"].append(photo_path)

    if message.document:
        document_path = await save_file(message.document.file_id, message.from_user.id)
        await insert_file_document(file_path = document_path)
        if "document_paths" not in task_info:
            task_info["document_paths"] = []
        task_info["document_paths"].append(document_path)

    print('файлы сохранены')
    return task_info

async def save_file(file_id, user_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    random_suffix = secrets.token_hex(8)  # Генерация случайной строки из 16 символов (8 байт в hex)
    destination = f"{SAVE_PATH}{user_id}/{user_id}_{random_suffix}_{os.path.basename(file_path)}"

    await bot.download_file(file_path, destination)
    return destination