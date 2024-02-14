import asyncio
from dotenv import load_dotenv
import os
import shlex
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery
from dbtools import delete_chat_id_from_alert, get_chat_sheet, init_db, create_pool, insert_chat_id_to_alert, insert_chat_sheet, get_all_chats, update_status_and_fetch_differences
from google_sheets.google_sheets_tools import fetch_rows_from_sheet

load_dotenv()
# python pip install python-dotenv aiogram asyncio gspread oauth2client asyncpg
bot_token = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv("DATABASE_URL")
SAVE_PATH = os.getenv('STATIC_PATH')
SHEET_URL = os.getenv('SHEET_URL')

if not bot_token:
    raise ValueError("No BOT_TOKEN found in your environment variables.")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

from markups import *
from incedent_handlers import *
from task_handlers import *
#Импорты аналитики
from tasks_handlers_categories.analitic.competitors_analitic import *
from tasks_handlers_categories.analitic.competitive_prices_analicit import *
from tasks_handlers_categories.analitic.analysis_sales_period import *
from tasks_handlers_categories.analitic.analysis_abc_xyz import *
#Импорты финансов
from tasks_handlers_categories.finance.finance_weekly_report import *
from tasks_handlers_categories.finance.finance_report_price_increase import *
from tasks_handlers_categories.finance.finance_price_elasticity import *
from tasks_handlers_categories.finance.financial_performance_report import *
#Импорты поставок
from tasks_handlers_categories.shipment.shipment_turnover_report import *
from tasks_handlers_categories.shipment.shipment_report_warehouses import *
from tasks_handlers_categories.shipment.shipment_create_delivery import *
from tasks_handlers_categories.shipment.shipment_calculation_delivery import *
from tasks_handlers_categories.shipment.shipment_acceptance_control import *
# Импорты контента
from tasks_handlers_categories.content.content_card_analysis import *
from tasks_handlers_categories.content.content_tk_photographer import *
from tasks_handlers_categories.content.content_tk_designer import *
from tasks_handlers_categories.content.content_creating_infographics import *
from tasks_handlers_categories.content.content_upload_image import *
from tasks_handlers_categories.content.content_new_card import*
from tasks_handlers_categories.content.content_update_card import*
from tasks_handlers_categories.content.content_collect_seo import *
# Импорты текстового контента
from tasks_handlers_categories.text_content.text_content_refresh import *
# Импорты свободной задачи
from tasks_handlers_categories.free.free_task import *
user_data = {}



@dp.message_handler(commands=['go'])
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

@dp.message_handler(commands=['registrationsheet'])
async def cmd_register_sheet(message: types.Message):
    args = shlex.split(message.get_args())
    if args:
        sheet_name = args[0]
        chat_id = message.chat.id
        user_id = message.from_user.id

        current_data = await get_chat_sheet(chat_id)
        table_link = current_data['table_link'] if current_data else ""

        try:
            await insert_chat_sheet(chat_id, sheet_name, user_id, table_link)
            await bot.send_message(chat_id=chat_id, text=f"Лист селлера '{sheet_name}' зарегистрирован в этом чате.")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Ошибка при регистрации листа селлера: '{sheet_name}'. \n {e}")
    else:
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, укажите название листа селлера после команды.")

@dp.message_handler(commands=['registrationlink'])
async def cmd_register_link(message: types.Message):
    args = shlex.split(message.get_args())
    if args:
        table_link = args[0]
        chat_id = message.chat.id
        user_id = message.from_user.id

        current_data = await get_chat_sheet(chat_id)
        sheet_name = current_data['sheet_name'] if current_data else ""

        try:
            await insert_chat_sheet(chat_id, sheet_name, user_id, table_link)
            await bot.send_message(chat_id=chat_id, text=f"Ссылка '{table_link}' зарегистрирована в этом чате.")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Ошибка при регистрации ссылки на таблицу: '{table_link}'. \n {e}")
    else:
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, укажите ссылку на таблицу после команды.")


@dp.message_handler(commands=['addnotify'])
async def cmd_register_link(message: types.Message):
    args = shlex.split(message.get_args())
    if args:
        sheet_name = args[0]
        chat_id = message.chat.id

        try:
            await insert_chat_id_to_alert(chat_id, sheet_name)
            await bot.send_message(chat_id=chat_id, text=f"Лист селлера '{sheet_name}' зарегистрирован в этом чате для уведомлений.")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Ошибка при регистрации листа селлера: '{sheet_name}'. \n {e}")
    else:
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, укажите название листа селлера после команды.")

@dp.message_handler(commands=['stopnotify'])
async def cmd_register_link(message: types.Message):
    args = shlex.split(message.get_args())
    if args:
        sheet_name = args[0]
        chat_id = message.chat.id

        try:
            await delete_chat_id_from_alert(chat_id, sheet_name)
            await bot.send_message(chat_id=chat_id, text=f"Лист селлера '{sheet_name}' убран из этого чата для уведомлений.")
        except Exception as e:
            await bot.send_message(chat_id=chat_id, text=f"Ошибка при удалении листа селлера: '{sheet_name}'. \n {e}")
    else:
        await bot.send_message(chat_id=message.chat.id, text="Пожалуйста, укажите название листа селлера после команды.")        

# Инцеденты
@dp.callback_query_handler(menu_cd.filter(action="incedent"))
async def process_incedent_type_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await incedent_type_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action=["seller_error", "manager_error", "marketplace_error"]))
async def process_seller_error_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await seller_error_incedent_handler(query, user_data, action, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_shipment"))
async def process_shipment_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    
    await shipment_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action="incedent_content"))
async def process_content_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_incedent_handler(query, user_data, **kwargs)

@dp.callback_query_handler(incedent_cd.filter(action=["incedent_content_infographic", "incedent_content_text", "incedent_content_data", "incedent_shipment_remains", "incedent_shipment_documents", "incedent_shipment_driver"]))
async def process_description_incedent_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await description_incedent_handler(query, user_data, action, **kwargs)

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

#
#Аналитика
#

#Анализ конкурентов
@dp.callback_query_handler(task_cd.filter(action="competitor_analysis"))
async def process_competitors_links_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await competitors_links_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "competitors_links")
async def process_input_competitors_links_handler(message: types.Message, **kwargs):
    await input_competitors_links_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_competitors_analitic_continue_without_links"))
async def process_input_competitors_description_handler_without_links(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_competitors_description_handler_without_links(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "competitors_analitic_description")
async def process_input_competitors_description_handler(message: types.Message, **kwargs):
    await input_competitors_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_competitors_analitic_continue_without_description"))
async def process_competitors_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await competitors_confirmation_handler_without_description(query, user_data, **kwargs)


#Анализ конкурентных цен
@dp.callback_query_handler(task_cd.filter(action="competitive_price_analysis"))
async def process_competitors_prices_links_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await competitors_prices_links_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "competitors_prices_links")
async def process_input_competitors_prices_links_handler(message: types.Message, **kwargs):
    await input_competitors_prices_links_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_competitors_prices_analitic_without_links"))
async def process_input_competitors_prices_description_handler_without_links(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_competitors_prices_description_handler_without_links(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "competitors_prices_analitic_description")
async def process_input_competitors_prices_description_handler(message: types.Message, **kwargs):
    await input_competitors_prices_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_competitors_prices_analitic_without_description"))
async def process_competitors_prices_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await competitors_prices_confirmation_handler_without_description(query, user_data, **kwargs)


#Анализ продаж за период
@dp.callback_query_handler(task_cd.filter(action="sales_period_analysis"))
async def process_period_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await period_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "sales_period_analysis_date")
async def process_input_period_date_handler(message: types.Message, **kwargs):
    await input_period_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_analysis_sales_period_continue_without_date"))
async def process_input_analysis_sales_period_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_analysis_sales_period_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "sales_period_analysis_description")
async def process_input_analysis_sales_period_description_handler(message: types.Message, **kwargs):
    await input_analysis_sales_period_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_analysis_sales_period_continue_without_description"))
async def process_analysis_sales_period_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await analysis_sales_period_confirmation_handler_without_description(query, user_data, **kwargs)


#Анализ ABC / XYZ
@dp.callback_query_handler(task_cd.filter(action="abc_xyz_analysis"))
async def process_analysis_abc_xyz_period_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await analysis_abc_xyz_period_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "analysis_abc_xyz_date")
async def process_input_analysis_abc_xyz_period_date_handler(message: types.Message, **kwargs):
    await input_analysis_abc_xyz_period_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_analysis_abc_xyz_continue_without_date"))
async def process_input_analysis_abc_xyz_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_analysis_abc_xyz_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "analysis_abc_xyz_description")
async def process_input_analysis_abc_xyz_description_handler(message: types.Message, **kwargs):
    await input_analysis_abc_xyz_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_analysis_abc_xyz_continue_without_description"))
async def process_analysis_abc_xyz_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await analysis_abc_xyz_confirmation_handler_without_description(query, user_data, **kwargs)


#
#Финансы
#

# Недельный финотчет
@dp.callback_query_handler(task_cd.filter(action="weekly_report_financial"))
async def process_finance_weekly_report_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_weekly_report_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_weekly_report_week")
async def process_input_finance_weekly_report_week_handler(message: types.Message, **kwargs):
    await input_finance_weekly_report_week_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_weekly_report_continue_without_week"))
async def process_input_finance_weekly_report_description_handler_without_week(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_finance_weekly_report_description_handler_without_week(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_weekly_report_description")
async def process_input_finance_weekly_report_description_handler(message: types.Message, **kwargs):
    await input_finance_weekly_report_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_weekly_report_continue_without_description"))
async def process_finance_weekly_report_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_weekly_report_confirmation_handler_without_description(query, user_data, **kwargs)


#Отчет после повышения цен
@dp.callback_query_handler(task_cd.filter(action="report_increase_financial"))
async def process_finance_report_price_increase_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_report_price_increase_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_report_price_increase_date")
async def process_input_finance_report_price_increase_date_handler(message: types.Message, **kwargs):
    await input_finance_report_price_increase_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_report_price_inc_continue_no_date"))
async def process_input_finance_report_price_increase_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_finance_report_price_increase_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_report_price_increase_description")
async def process_input_finance_report_price_increase_description_handler(message: types.Message, **kwargs):
    await input_finance_report_price_increase_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_report_price_inc_continue_no_description"))
async def process_finance_report_price_increase_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_report_price_increase_confirmation_handler_without_description(query, user_data, **kwargs)

#Эластичность цены
@dp.callback_query_handler(task_cd.filter(action="price_elasticity_financial"))
async def process_finance_price_elasticity_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_price_elasticity_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_price_elasticity_date")
async def process_input_finance_price_elasticity_date_handler(message: types.Message, **kwargs):
    await input_finance_price_elasticity_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_price_elasticity_continue_no_date"))
async def process_input_finance_price_elasticity_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_finance_price_elasticity_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "finance_price_elasticity_description")
async def process_input_finance_price_elasticity_description_handler(message: types.Message, **kwargs):
    await input_finance_price_elasticity_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_finance_price_elasticity_continue_no_description"))
async def process_finance_price_elasticity_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await finance_price_elasticity_confirmation_handler_without_description(query, user_data, **kwargs)

#Отчет о проделанной работе в разрезе финансовых показателей
@dp.callback_query_handler(task_cd.filter(action="report_section_financial"))
async def process_financial_performance_report_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await financial_performance_report_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "financial_performance_report_date")
async def process_input_financial_performance_report_date_handler(message: types.Message, **kwargs):
    await input_financial_performance_report_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_financial_performance_report_continue_no_date"))
async def process_input_financial_performance_report_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_financial_performance_report_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "financial_performance_report_description")
async def process_input_financial_performance_report_description_handler(message: types.Message, **kwargs):
    await input_financial_performance_report_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_financial_performance_report_continue_no_description"))
async def process_financial_performance_report_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await financial_performance_report_confirmation_handler_without_description(query, user_data, **kwargs)

#
#Поставки
#

#Отчет оборачиваемости
@dp.callback_query_handler(task_cd.filter(action="turnover_report_shipment"))
async def process_shipment_turnover_report_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_turnover_report_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_turnover_report_date")
async def process_input_shipment_turnover_report_date_handler(message: types.Message, **kwargs):
    await input_shipment_turnover_report_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_turnover_report_continue_no_date"))
async def process_input_shipment_turnover_report_goods_ids_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_shipment_turnover_report_goods_ids_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_turnover_report_goods_ids")
async def process_input_shipment_turnover_report_description_handler(message: types.Message, **kwargs):
    await input_shipment_turnover_report_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_turnover_report_continue_no_goods_ids"))
async def process_input_shipment_turnover_report_description_handler_without_goods_ids(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_shipment_turnover_report_description_handler_without_goods_ids(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_turnover_report_continue_all_goods_ids"))
async def process_input_shipment_turnover_report_description_handler_all_goods_ids(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_shipment_turnover_report_description_handler_all_goods_ids(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_turnover_report_description")
async def process_input_shipment_turnover_report_confirmation_handler(message: types.Message, **kwargs):
    await input_shipment_turnover_report_confirmation_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_turnover_report_continue_no_description"))
async def process_shipment_turnover_report_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_turnover_report_confirmation_handler_without_description(query, user_data, **kwargs)


#Отчет по остаткам с разбивкой по складам
@dp.callback_query_handler(task_cd.filter(action="report_warehouses_shipment"))
async def process_shipment_report_warehouses_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_report_warehouses_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_report_warehouses_date")
async def process_input_shipment_report_warehouses_date_handler(message: types.Message, **kwargs):
    await input_shipment_report_warehouses_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_report_warehouses_continue_no_date"))
async def process_input_shipment_report_warehouses_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_shipment_report_warehouses_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_report_warehouses_description")
async def process_input_shipment_report_warehouses_description_handler(message: types.Message, **kwargs):
    await input_shipment_report_warehouses_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_report_warehouses_continue_no_description"))
async def process_shipment_report_warehouses_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_report_warehouses_confirmation_handler_without_description(query, user_data, **kwargs)


#Расчет поставки на склад
@dp.callback_query_handler(task_cd.filter(action="calculation_delivery_shipment"))
async def process_shipment_calculation_delivery_warehouse_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_calculation_delivery_warehouse_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action=["task_shipment_calculation_delivery_continue_center", "task_shipment_calculation_delivery_continue_region", "task_shipment_calculation_delivery_continue_all"]))
async def process_input_shipment_calculation_delivery_warehouse_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await input_shipment_calculation_delivery_warehouse_handler(query, user_data, action, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_calculation_delivery_description")
async def process_input_shipment_calculation_delivery_description_handler(message: types.Message, **kwargs):
    await input_shipment_calculation_delivery_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_calculation_delivery_continue_no_description"))
async def process_shipment_calculation_delivery_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_calculation_delivery_confirmation_handler_without_description(query, user_data, **kwargs)


#Создать поставку


@dp.callback_query_handler(task_cd.filter(action="create_delivery_shipment"))
async def process_shipment_create_delivery_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_create_delivery_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action=["task_shipment_create_prev_data", "task_shipment_create_contact"]))
async def process_input_shipment_create_delivery_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await input_shipment_create_delivery_type_handler(query, user_data, action, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_create_delivery_description")
async def process_input_shipment_create_delivery_description_handler(message: types.Message, **kwargs):
    await input_shipment_create_delivery_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_create_delivery_continue_no_description"))
async def process_shipment_create_delivery_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_create_delivery_confirmation_handler_without_description(query, user_data, **kwargs)



#Контроль приемки
@dp.callback_query_handler(task_cd.filter(action="acceptance_control_shipment"))
async def process_shipment_acceptance_control_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_acceptance_control_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_acceptance_control_date")
async def process_input_shipment_acceptance_control_date_handler(message: types.Message, **kwargs):
    await input_shipment_acceptance_control_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_acceptance_control_continue_no_date"))
async def process_input_shipment_acceptance_control_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_shipment_acceptance_control_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "shipment_acceptance_control_description")
async def process_input_shipment_acceptance_control_description_handler(message: types.Message, **kwargs):
    await input_shipment_acceptance_control_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_shipment_acceptance_control_continue_no_description"))
async def process_shipment_acceptance_control_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await shipment_acceptance_control_confirmation_handler_without_description(query, user_data, **kwargs)


#
# Контент
#

#Анализ карточки
@dp.callback_query_handler(task_cd.filter(action="card_analysis_content"))
async def process_content_card_analysis_skus_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_card_analysis_skus_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_card_analysis_goods_ids")
async def process_input_content_card_analysis_description_handler(message: types.Message, **kwargs):
    await input_content_card_analysis_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_card_analysis_continue_no_goods_ids"))
async def process_input_content_card_analysis_description_handler_without_goods_ids(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_card_analysis_description_handler_without_goods_ids(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_card_analysis_continue_all_goods_ids"))
async def process_input_content_card_analysis_description_handler_all_goods_ids(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_card_analysis_description_handler_all_goods_ids(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_card_analysis_description")
async def process_input_content_card_analysis_confirmation_handler(message: types.Message, **kwargs):
    await input_content_card_analysis_confirmation_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_card_analysis_continue_no_description"))
async def process_content_card_analysis_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_card_analysis_confirmation_handler_without_description(query, user_data, **kwargs)


#ТЗ для фотографа
@dp.callback_query_handler(task_cd.filter(action="tk_photographer_content"))
async def process_content_tk_photographer_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_tk_photographer_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_tk_photographer_date", content_types=['text', 'photo', 'document'])
async def process_input_content_tk_photographer_date_handler(message: types.Message, **kwargs):
    print('start handler')
    await input_content_tk_photographer_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_tk_photographer_continue_no_date"))
async def process_input_content_tk_photographer_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_tk_photographer_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_tk_photographer_description")
async def process_input_content_tk_photographer_description_handler(message: types.Message, **kwargs):
    await input_content_tk_photographer_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_tk_photographer_continue_no_description"))
async def process_content_tk_photographer_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_tk_photographer_confirmation_handler_without_description(query, user_data, **kwargs)


#ТЗ для дизайнера
@dp.callback_query_handler(task_cd.filter(action="tk_designer_content"))
async def process_content_tk_designer_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_tk_designer_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_tk_designer_date", content_types=['text', 'photo', 'document'])
async def process_input_content_tk_designer_date_handler(message: types.Message, **kwargs):
    await input_content_tk_designer_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_tk_designer_continue_no_date"))
async def process_input_content_tk_designer_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_tk_designer_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_tk_designer_description")
async def process_input_content_tk_designer_description_handler(message: types.Message, **kwargs):
    await input_content_tk_designer_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_tk_designer_continue_no_description"))
async def process_content_tk_designer_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_tk_designer_confirmation_handler_without_description(query, user_data, **kwargs)


#Создание инфографики
@dp.callback_query_handler(task_cd.filter(action="infographics_content"))
async def process_content_creating_infographics_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_creating_infographics_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_creating_infographics_date", content_types=['text', 'photo', 'document'])
async def process_input_content_creating_infographics_date_handler(message: types.Message, **kwargs):
    await input_content_creating_infographics_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_creating_infographics_continue_no_date"))
async def process_input_content_creating_infographics_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_creating_infographics_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_creating_infographics_description")
async def process_input_content_creating_infographics_description_handler(message: types.Message, **kwargs):
    await input_content_creating_infographics_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_creating_infographics_continue_no_description"))
async def process_content_creating_infographics_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_creating_infographics_confirmation_handler_without_description(query, user_data, **kwargs)


#Загрузить новое изображение
@dp.callback_query_handler(task_cd.filter(action="new_image_content"))
async def process_content_upload_image_action_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_upload_image_action_handler(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action=["task_content_upload_image_change","task_content_upload_image_new"]))
async def process_input_content_upload_image_task_type_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await input_content_upload_image_task_type_handler(query, user_data, action, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_upload_image_file")
async def process_input_content_upload_image_date_handler(message: types.Message, **kwargs):
    await input_content_upload_image_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_upload_image_continue_no_photo"))
async def process_input_content_upload_image_description_handler_without_data(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_upload_image_description_handler_without_data(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_upload_image_description")
async def process_input_content_upload_image_confirmation_handler(message: types.Message, **kwargs):
    await input_content_upload_image_confirmation_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_upload_image_continue_no_description"))
async def process_content_upload_image_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_upload_image_confirmation_handler_without_description(query, user_data, **kwargs)

#Создание новой карточки
@dp.callback_query_handler(task_cd.filter(action="new_card_content"))
async def process_content_new_card_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_new_card_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_new_card_date", content_types=['text', 'photo', 'document'])
async def process_input_content_new_card_date_handler(message: types.Message, **kwargs):
    print('start handler')
    await input_content_new_card_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_new_card_continue_no_date"))
async def process_input_content_new_card_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_new_card_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_new_card_description")
async def process_input_content_new_card_description_handler(message: types.Message, **kwargs):
    await input_content_new_card_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_new_card_continue_no_description"))
async def process_content_new_card_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_new_card_confirmation_handler_without_description(query, user_data, **kwargs)

#Обновление карточки
@dp.callback_query_handler(task_cd.filter(action="update_card_content"))
async def process_content_update_card_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_update_card_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_update_card_date", content_types=['text', 'photo', 'document'])
async def process_input_content_update_card_date_handler(message: types.Message, **kwargs):
    print('start handler')
    await input_content_update_card_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_update_card_continue_no_date"))
async def process_input_content_update_card_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_update_card_description_handler_without_date(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_update_card_description")
async def process_input_content_update_card_description_handler(message: types.Message, **kwargs):
    await input_content_update_card_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_update_card_continue_no_description"))
async def process_content_update_card_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_update_card_confirmation_handler_without_description(query, user_data, **kwargs)

#Собрать SEO
@dp.callback_query_handler(task_cd.filter(action="collect_seo_content"))
async def process_content_collect_seo_skus_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_collect_seo_skus_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_collect_seo_goods_ids")
async def process_input_content_collect_seo_description_handler(message: types.Message, **kwargs):
    await input_content_collect_seo_description_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_collect_seo_continue_no_goods_ids"))
async def process_input_content_collect_seo_description_handler_without_goods_ids(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_content_collect_seo_description_handler_without_goods_ids(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "content_collect_seo_description")
async def process_input_content_collect_seo_confirmation_handler(message: types.Message, **kwargs):
    await input_content_collect_seo_confirmation_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_collect_seo_continue_no_description"))
async def process_content_collect_seo_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await content_collect_seo_confirmation_handler_without_description(query, user_data, **kwargs)


#
# Обновить текстовый контент
#
@dp.callback_query_handler(task_cd.filter(action="task_refresh_content"))
async def process_text_content_refresh_sku_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await text_content_refresh_sku_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "text_content_refresh_date")
async def process_input_text_content_refresh_type_handler(message: types.Message, **kwargs):
    await input_text_content_refresh_type_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action=["task_content_refresh_product_name","task_content_refresh_product_description","task_content_refresh_product_charact","task_content_refresh_products_seo"]))
async def process_input_text_content_refresh_task_type_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    action = callback_data.get('action')
    await input_text_content_refresh_task_type_handler(query, user_data, action, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "text_content_refresh_file", content_types=['text', 'photo', 'document'])
async def process_input_text_content_refresh_file_handler(message: types.Message, **kwargs):
    await input_text_content_refresh_file_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_refresh_continue_no_data"))
async def process_input_text_content_refresh_description_handler_without_data(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_text_content_refresh_description_handler_without_data(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_content_refresh_continue_no_description"))
async def process_text_content_refresh_confirmation_handler_without_description(query: CallbackQuery, callback_data: dict, **kwargs):
    await text_content_refresh_confirmation_handler_without_description(query, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="task_confirm"))
async def process_confirm_task(query: CallbackQuery, callback_data: dict, **kwargs):
    await confirmed_task(query, user_data, **kwargs)


#Свободная задача
@dp.callback_query_handler(task_cd.filter(action="task_free"))
async def process_free_task_date_handler(query: CallbackQuery, callback_data: dict, **kwargs):
    await free_task_date_handler(query, user_data, **kwargs)

@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id].get("current_message") == "free_task_date", content_types=['text', 'photo', 'document'])
async def process_input_free_task_date_handler(message: types.Message, **kwargs):
    print('start handler')
    await input_free_task_date_handler(message, user_data, **kwargs)

@dp.callback_query_handler(task_cd.filter(action="free_task_continue"))
async def process_input_free_task_description_handler_without_date(query: CallbackQuery, callback_data: dict, **kwargs):
    await input_free_task_description_handler_without_date(query, user_data, **kwargs)

async def notify():
    chats = await get_all_chats()
    for chat in chats:
      rows =  await fetch_rows_from_sheet(chat["table_link"], chat["sheet_name"])
      updated_rows = await update_status_and_fetch_differences(rows)
      for row in updated_rows:
        alert_message = (
          "У задачи:\n"
          f"{row['info']}\n"
          f"Изменился статус на {row['status']}"
        )
        print(alert_message)
        await bot.send_message(
          chat_id=chat['chat_id'],
          text=alert_message,
        )

async def notify_periodically():
    while True:
        print("Запуск notify")
        await notify()
        print("Завершение notify, ожидание следующего вызова...")
        await asyncio.sleep(300)

async def main():
    print('start')
    await create_pool()
    print('create pool')
    await init_db()
    print('init_db')
    asyncio.create_task(dp.start_polling())
    print('dp.start_polling')
    notify_task = asyncio.create_task(notify_periodically())
    
    await notify_task

if __name__ == '__main__':
    asyncio.run(main())
