from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from dbtools import update_status_and_fetch_differences
import os

load_dotenv()

def transform_paths(paths):
    current_host = os.getenv('HOST_NAME')
    return [current_host + '/'.join(path.split('/')[2:]) for path in paths]

def add_row_to_sheet(sheet_url, sheet_name, task_info, task_id):
    # Авторизация и получение таблицы
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/bot-task-tracker-2cbdc3a7ab62.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

    # Находим первую пустую строку
    all_values = sheet.col_values(2)  # Проверка второго столбца для нахождения пустой строки
    empty_row = len(all_values) + 1
    for i, value in enumerate(all_values, start=1):
        if value == '':
            empty_row = i
            break

    # Собираем данные для записи
    task_category = task_info.get('task_category', '')
    task_date = datetime.now().strftime('%Y-%m-%d')
    
    # Словарь описаний для ключей информации
    info_descriptions = {
        'task_subcategory': 'субкатегория задачи',
        'period_date': 'период',
        'task_description': 'описание задачи',
        'competitors_links': 'ссылки на конкурентов',
        'goods_sku': 'sku товаров',
        'goods_info': 'инфо товаров',
        'task_action': 'действие задачи',
        'task_report_week': 'отчетная неделя',
        'warehouse': 'склад'
    }

    # Собираем данные для записи с описаниями, исключая значения равные '-'
    info_keys = list(info_descriptions.keys())
    info_values = [f"{info_descriptions[key]}: {task_info.get(key, '')}" 
                   for key in info_keys if task_info.get(key, '') != '-']

    # Преобразование путей фотографий и документов
    photo_paths = [path for path in transform_paths(task_info.get('photo_paths', [])) if path != '-']
    document_paths = [path for path in transform_paths(task_info.get('document_paths', [])) if path != '-']

    # Добавление URL фото и документов в combined_info, если они не равны '-'
    if photo_paths:
        info_values.append('Фотографии:\n' + '\n'.join(photo_paths))
    if document_paths:
        info_values.append('Документы:\n' + '\n'.join(document_paths))

    # Добавление строки "Задача:" в начало списка info_values
    info_values.insert(0, "Задача:")

    combined_info = '\n'.join(info_values)

    # Обновление данных в таблице, включая task_id в столбец 'A'
    sheet.update(f'A{empty_row}', [[task_id]])                      # ID задачи
    sheet.update(f'J{empty_row}:J{empty_row}', [[task_category]])   # Категория задачи
    sheet.update(f'B{empty_row}:B{empty_row}', [[task_date]])       # Дата задачи
    sheet.update(f'F{empty_row}:F{empty_row}', [[combined_info]])   # Объединенная информацияи


def add_incedent_row_to_sheet(sheet_url, sheet_name, incident_info, incident_id):
    # Авторизация и получение таблицы
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/bot-task-tracker-2cbdc3a7ab62.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

    # Находим первую пустую строку
    all_values = sheet.col_values(2)  # Предполагается, что колонка B используется для проверки пустых строк
    empty_row = len(all_values) + 1
    for i, value in enumerate(all_values, start=1):
        if value == '':
            empty_row = i
            break

    # Собираем данные для записи
    incident_type = incident_info.get('type', '')
    work_category = incident_info.get('work_category', '')
    incident_description = incident_info.get('incedent_description', '')

    incident_info_combined = f'Инцидент:\n{incident_type}\n{incident_description}'
    incident_date = datetime.now().strftime('%Y-%m-%d')

    # Обновление данных в таблице, включая incident_id в столбец 'A'
    sheet.update(f'A{empty_row}', [[incident_id]])                        # ID инцидента
    sheet.update(f'F{empty_row}:F{empty_row}', [[incident_info_combined]]) # Информация об инциденте
    sheet.update(f'J{empty_row}:J{empty_row}', [[work_category]])         # Категория работы
    sheet.update(f'B{empty_row}:B{empty_row}', [[incident_date]])



async def fetch_rows_from_sheet(sheet_url, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/bot-task-tracker-2cbdc3a7ab62.json', scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    except gspread.exceptions.NoValidUrlKeyFound:
        print(f"URL {sheet_url} не содержит действительного ключа документа.")
        return []
    except gspread.exceptions.WorksheetNotFound:
        print(f"Лист {sheet_name} не найден.")
        return []

    try:
        ids = sheet.col_values(1)
        dates = sheet.col_values(2)
        deadlines = sheet.col_values(4)
        infos = sheet.col_values(6)
        statuses = sheet.col_values(9)
    except Exception as e:
        print(f"Произошла ошибка при получении данных из листа: {e}")
        return []

    min_length = min(len(ids), len(dates), len(deadlines), len(infos), len(statuses))

    rows = []
    for i in range(1, min_length):
        type_info = "Неизвестно"
        info = infos[i] if i < len(infos) else ""
        status = statuses[i] if i < len(statuses) else ""
        date = dates[i] if i < len(dates) else ""
        deadline = deadlines[i] if i < len(deadlines) and deadlines[i] != "" else "-"

        if info.startswith("Инцидент"):
            type_info = "Инцидент"
        elif info.startswith("Задача"):
            type_info = "Задача"

        row_object = {
            "id": ids[i],
            "type": type_info,
            "status": status,
            "info": info,
            "date": date,
            "deadline": deadline,
        }
        rows.append(row_object)

    return rows
