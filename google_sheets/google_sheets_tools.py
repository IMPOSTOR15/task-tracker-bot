import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Функция для добавления строки в Google Sheets
def add_row_to_sheet(sheet_url, sheet_name, task_info):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials/bot-task-tracker-2cbdc3a7ab62.json', scope)

    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)

    # Находим первую пустую строку в столбце B
    all_values = sheet.col_values(2)  # Столбец B
    empty_row = len(all_values) + 1
    for i, value in enumerate(all_values, start=1):
        if value == '':
            empty_row = i
            break

    # Собираем данные для записи
    task_category = task_info.get('task_category', '')
    task_date = datetime.now().strftime('%Y-%m-%d')  # Текущая дата

    # Игнорируем ключи 'add_by_user_id' и 'chat_id'
    info_keys = ['task_subcategory', 'period_date', 'task_description', 'competitors_links', 
                 'goods_sku', 'goods_info', 'task_action', 'task_report_week', 'warehouse']
    info_values = [task_info.get(key, '') for key in info_keys if key in task_info]
    combined_info = '\n'.join(info_values)  # Каждое значение с новой строки

    # Запись данных в таблицу
    data_to_insert = [task_category, task_date, combined_info]
    sheet.update(f'J{empty_row}:J{empty_row}', [[task_category]])  # Запись в столбец J
    sheet.update(f'B{empty_row}:B{empty_row}', [[task_date]])     # Запись в столбец B
    sheet.update(f'F{empty_row}:F{empty_row}', [[combined_info]])  # Запись в столбец F