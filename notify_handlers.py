from dbtools import get_all_chats, update_status_and_fetch_differences
from google_sheets.google_sheets_tools import fetch_rows_from_sheet
from main import bot

async def notify():
    chats = await get_all_chats()
    for chat in chats:
      rows =  await fetch_rows_from_sheet(chat["table_link"], chat["sheet_name"])
      updated_rows = await update_status_and_fetch_differences()
      for row in updated_rows:
        alert_message = (
          "У задачи:\n"
          f"{row['info']}\n"
          f"Изменился статус на {row['status']}"
        )   
        await bot.send_message(
          chat_id=chat['chat_id'],
          text=alert_message,
        )
