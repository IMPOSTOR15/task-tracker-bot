import os
from aiogram import types
from main import bot, SAVE_PATH

async def process_media(message: types.Message, task_info):
    """
    Обработка медиафайлов в сообщении.

    :param message: Объект сообщения, содержащего медиа.
    :param task_info: Словарь данных пользователя для сохранения путей к файлам.
    :return: Обновленный task_info с путями к фото и документам.
    """
    # Обработка фотографий
    if message.photo:
        # Получаем фотографию с самым высоким разрешением
        highest_resolution_photo = message.photo[-1]
        photo_path = await save_file(highest_resolution_photo.file_id, message.from_user.id)
        if "photo_paths" not in task_info:
            task_info["photo_paths"] = []
        task_info["photo_paths"].append(photo_path)
    else:
        task_info["photo_paths"] = '-'
    # Обработка документа
    if message.document:
        document_path = await save_file(message.document.file_id, message.from_user.id)

        if "document_paths" not in task_info:
            task_info["document_paths"] = []
        task_info["document_paths"].append(document_path)
    else:
        task_info["document_path"] = '-'
    print('файлы сохранены')
    return task_info

async def save_file(file_id, user_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    destination = f"{SAVE_PATH}{user_id}/{user_id}_{os.path.basename(file_path)}"
    await bot.download_file(file_path, destination)
    return destination