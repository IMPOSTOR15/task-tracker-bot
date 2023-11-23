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
    
    # Обработка основной информации
    info_keys = ['task_subcategory', 'period_date', 'task_description', 'competitors_links', 
                 'goods_sku', 'goods_info', 'task_action', 'task_report_week', 'warehouse']
    info_values = [task_info.get(key, '') for key in info_keys if key in task_info]

    # Преобразование путей фотографий и документов и добавление их в основную информацию
    photo_paths = transform_paths(task_info.get('photo_paths', []))
    document_paths = transform_paths(task_info.get('document_paths', []))
    # Добавление URL фото и документов в combined_info
    if photo_paths:
        info_values.append('Photo URLs:\n' + '\n'.join(photo_paths))
    if document_paths:
        info_values.append('Document URLs:\n' + '\n'.join(document_paths))

    combined_info = '\n'.join(info_values)

    # Обновление данных в таблице
    sheet.update(f'J{empty_row}:J{empty_row}', [[task_category]])  # Категория задачи
    sheet.update(f'B{empty_row}:B{empty_row}', [[task_date]])     # Дата задачи
    sheet.update(f'F{empty_row}:F{empty_row}', [[combined_info]])  # Объединенная информация
