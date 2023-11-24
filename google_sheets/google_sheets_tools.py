from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()

def transform_paths(paths):
    current_host = os.getenv('HOST_NAME')
    return [current_host + '/'.join(path.split('/')[2:]) for path in paths]

def add_row_to_sheet(sheet_url, sheet_name, task_info):

    # Авторизация и получение таблицы
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/bot-task-tracker-2cbdc3a7ab62.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

    # Находим первую пустую строку
    all_values = sheet.col_values(2)
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

    # Преобразование путей фотографий и документов, исключая значения равные '-'
    photo_paths = [path for path in transform_paths(task_info.get('photo_paths', [])) if path != '-']
    document_paths = [path for path in transform_paths(task_info.get('document_paths', [])) if path != '-']

    # Добавление URL фото и документов в combined_info, если они не равны '-'
    if photo_paths:
        info_values.append('Фотографии:\n' + '\n'.join(photo_paths))
    if document_paths:
        info_values.append('Документы:\n' + '\n'.join(document_paths))

    combined_info = '\n'.join(info_values)

    # Обновление данных в таблице
    sheet.update(f'J{empty_row}:J{empty_row}', [[task_category]])  # Категория задачи
    sheet.update(f'B{empty_row}:B{empty_row}', [[task_date]])     # Дата задачи
    sheet.update(f'F{empty_row}:F{empty_row}', [[combined_info]])  # Объединенная информация


def add_incedent_row_to_sheet(sheet_url, sheet_name, incident_info):
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

    incedent_info = f'{incident_type}\n{incident_description}'
    incident_date = datetime.now().strftime('%Y-%m-%d')

    # Обновление данных в таблице
    sheet.update(f'F{empty_row}:F{empty_row}', [[incedent_info]])
    sheet.update(f'J{empty_row}:J{empty_row}', [[work_category]])
    sheet.update(f'B{empty_row}:B{empty_row}', [[incident_date]])