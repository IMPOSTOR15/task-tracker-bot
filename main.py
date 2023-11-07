import asyncio
from dotenv import load_dotenv
import os
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.utils.callback_data import CallbackData


from markups import *
from incedent_handlers import *
from task_handlers import *

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
if not bot_token:
    raise ValueError("No BOT_TOKEN found in your environment variables.")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)
print(dp)

user_data = {}

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_data["user_id"] = message.from_user.id
    keyboard_markup = await main_task_keyboard()
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот трекер задач."
                        "\nЯ могу создавать задачи для команды"
                        "\nВыбери какой тип задачи тебя интерсует", 
                        reply_markup=keyboard_markup)
    
@dp.callback_query_handler(menu_cd.filter(action="back"))
async def back_to_main_menu(query: CallbackQuery):
    user_data["user_id"] = query.message.from_user.id
    keyboard_markup = await main_task_keyboard()
    await bot.edit_message_text(chat_id=query.message.chat.id,
                                message_id=query.message.message_id,
                                text="Привет! Я бот трекер задач."
                                     "\nЯ могу создавать задачи для команды"
                                     "\nВыбери какой тип задачи тебя интерсует",
                                reply_markup=keyboard_markup)
    await query.answer()


# Инцеденты
@dp.callback_query_handler(menu_cd.filter(action="incedent"))
async def process_incedent_type_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await incedent_type_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="seller_error"))
async def process_seller_error_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await seller_error_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="manager_error"))
async def process_manager_error_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await manager_error_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="marketplace_error"))
async def process_marketplace_error_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await marketplace_error_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_shipment"))
async def process_shipment_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_content"))
async def process_content_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action=["incedent_content_infographic", "incedent_content_text", "incedent_content_data", "incedent_shipment_remains", "incedent_shipment_documents", "incedent_shipment_driver"]))
async def process_description_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await description_incedent_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "description_incedent")
async def process_description_incedent_input(message: types.Message, **kwargs):
    await description_incedent_input(message, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_continue_without_description"))
async def process_description_incedent_input_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await description_incedent_input_without_description(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_confirm"))
async def process_confirm_incedent(query: CallbackQuery, callback_data: dict, **kwargs):
    await confirmed_incedent(query, user_data, **kwargs)

# Задачи
@dp.callback_query_handler(menu_cd.filter(action="task"))
async def process_task_work_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_work_handler(query, user_data, **kwargs)

# Типы задач
@dp.callback_query_handler(task_cd.filter(action="task_analitic"))
async def process_task_analitic_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_analitic_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance"))
async def process_task_finance_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_finance_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_delivery"))
async def process_task_shipment_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_shipment_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content"))
async def process_task_content_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_content_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_refresh_content"))
async def process_refresh_content_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await task_refresh_content_handler(query, user_data, **kwargs)


async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
