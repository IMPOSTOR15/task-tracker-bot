import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from markups import back_button, menu_cd
task_cd = CallbackData("task", "action")


async def task_work_keyboard():
    keyboard = InlineKeyboardMarkup()
    analitic_task_work_btn = InlineKeyboardButton("Аналитика", callback_data=task_cd.new(action="task_analitic"))
    finance_task_work_btn = InlineKeyboardButton("Финансы", callback_data=task_cd.new(action="task_finance"))
    delivery_task_work_btn = InlineKeyboardButton("Поставки", callback_data=task_cd.new(action="task_delivery"))
    content_task_work_btn = InlineKeyboardButton("Контент", callback_data=task_cd.new(action="task_content"))
    refresh_content_task_work_btn = InlineKeyboardButton("Обновить текстовый контент", callback_data=task_cd.new(action="task_refresh_content"))
    free_task_btn = InlineKeyboardButton("Свободная задача", callback_data=task_cd.new(action="task_free"))

    keyboard.add(analitic_task_work_btn)
    keyboard.add(finance_task_work_btn)
    keyboard.add(delivery_task_work_btn)
    keyboard.add(content_task_work_btn)
    keyboard.add(refresh_content_task_work_btn)
    keyboard.add(free_task_btn)
    keyboard.add(back_button())
    return keyboard

async def task_analitic_keyboard():
    keyboard = InlineKeyboardMarkup()
    competitor_analysis_task_btn = InlineKeyboardButton("Анализ конкурентов", callback_data=task_cd.new(action="competitor_analysis"))
    competitive_price_analysis_task_btn = InlineKeyboardButton("Анализ конкурентных цен", callback_data=task_cd.new(action="competitive_price_analysis"))
    analysis_sales_period_task_btn = InlineKeyboardButton("Анализ продаж за период", callback_data=task_cd.new(action="sales_period_analysis"))
    abc_xyz_analysis_task_btn = InlineKeyboardButton("Анализ ABC / XYZ", callback_data=task_cd.new(action="abc_xyz_analysis"))

    keyboard.add(competitor_analysis_task_btn)
    keyboard.add(competitive_price_analysis_task_btn)
    keyboard.add(analysis_sales_period_task_btn)
    keyboard.add(abc_xyz_analysis_task_btn)
    keyboard.add(back_button(action_name = "task"))
    return keyboard

async def task_finance_keyboard():
    keyboard = InlineKeyboardMarkup()
    weekly_report_financial_task_btn = InlineKeyboardButton("Недельный финотчет", callback_data=task_cd.new(action="weekly_report_financial"))
    report_after_price_increase_financial_task_btn = InlineKeyboardButton("Отчет после повышения цен", callback_data=task_cd.new(action="report_increase_financial"))
    price_elasticity_financial_task_btn = InlineKeyboardButton("Эластичность цены", callback_data=task_cd.new(action="price_elasticity_financial"))
    report_section_financial_task_btn = InlineKeyboardButton("Отчет о работе в разрезе фин. показателей", callback_data=task_cd.new(action="report_section_financial"))

    keyboard.add(weekly_report_financial_task_btn)
    keyboard.add(report_after_price_increase_financial_task_btn)
    keyboard.add(price_elasticity_financial_task_btn)
    keyboard.add(report_section_financial_task_btn)
    keyboard.add(back_button(action_name = "task"))
    return keyboard


async def task_shipment_keyboard():
    keyboard = InlineKeyboardMarkup()
    turnover_report_shipment_task_btn = InlineKeyboardButton("Отчет оборачиваемости", callback_data=task_cd.new(action="turnover_report_shipment"))
    report_warehouses_shipment_task_btn = InlineKeyboardButton("Отчет по остаткам с разбивкой по складам", callback_data=task_cd.new(action="report_warehouses_shipment"))
    calculation_delivery_shipment_task_btn = InlineKeyboardButton("Расчет поставки на склад", callback_data=task_cd.new(action="calculation_delivery_shipment"))
    create_delivery_shipment_task_btn = InlineKeyboardButton("Создать поставку", callback_data=task_cd.new(action="create_delivery_shipment"))
    acceptance_control_shipment_task_btn = InlineKeyboardButton("Контроль приемки", callback_data=task_cd.new(action="acceptance_control_shipment"))

    keyboard.add(turnover_report_shipment_task_btn)
    keyboard.add(report_warehouses_shipment_task_btn)
    keyboard.add(calculation_delivery_shipment_task_btn)
    keyboard.add(create_delivery_shipment_task_btn)
    keyboard.add(acceptance_control_shipment_task_btn)
    keyboard.add(back_button(action_name = "task"))
    return keyboard

async def task_content_keyboard():
    keyboard = InlineKeyboardMarkup()
    card_analysis_content_task_btn = InlineKeyboardButton("Анализ карточки", callback_data=task_cd.new(action="card_analysis_content"))
    tk_photographer_content_task_btn = InlineKeyboardButton("ТЗ для фотографа", callback_data=task_cd.new(action="tk_photographer_content"))
    tk_designer_content_task_btn = InlineKeyboardButton("ТЗ для дизайнера", callback_data=task_cd.new(action="tk_designer_content"))
    infographics_content_task_btn = InlineKeyboardButton("Создание инфографики", callback_data=task_cd.new(action="infographics_content"))
    new_image_content_task_btn = InlineKeyboardButton("Загрузить новое изображение", callback_data=task_cd.new(action="new_image_content"))
    new_card_content_task_btn = InlineKeyboardButton("Создать новую карточку", callback_data=task_cd.new(action="new_card_content"))
    upd_card_content_task_btn = InlineKeyboardButton("Изменить существующую карточку", callback_data=task_cd.new(action="update_card_content"))
    collect_seo_content_task_btn = InlineKeyboardButton("Собрать SEO", callback_data=task_cd.new(action="collect_seo_content"))

    keyboard.add(card_analysis_content_task_btn)
    keyboard.add(tk_photographer_content_task_btn)
    keyboard.add(tk_designer_content_task_btn)
    keyboard.add(infographics_content_task_btn)
    keyboard.add(new_image_content_task_btn)
    keyboard.add(new_card_content_task_btn)
    keyboard.add(upd_card_content_task_btn)
    keyboard.add(collect_seo_content_task_btn)
    keyboard.add(back_button(action_name = "task"))
    return keyboard

async def task_refresh_content_keyboard():
    keyboard = InlineKeyboardMarkup()
    title_refresh_task_btn = InlineKeyboardButton("Название", callback_data=task_cd.new(action="title_refresh"))
    description_refresh_task_btn = InlineKeyboardButton("Описание", callback_data=task_cd.new(action="description_refresh"))
    specifications_refresh_task_btn = InlineKeyboardButton("Характеристики", callback_data=task_cd.new(action="specifications_refresh"))
    seo_refresh_task_btn = InlineKeyboardButton("SEO", callback_data=task_cd.new(action="seo_refresh"))

    keyboard.add(title_refresh_task_btn)
    keyboard.add(description_refresh_task_btn)
    keyboard.add(specifications_refresh_task_btn)
    keyboard.add(seo_refresh_task_btn)
    keyboard.add(back_button(action_name = "task"))
    return keyboard

async def task_confirm_keyboard():
    keyboard = InlineKeyboardMarkup()
    confirm_btn = InlineKeyboardButton("Подтвердить", callback_data=task_cd.new(action="task_confirm"))
    again_btn = InlineKeyboardButton("Заполнить заново", callback_data=menu_cd.new(action="back"))
    keyboard.add(confirm_btn)
    keyboard.add(again_btn)
    return keyboard

async def task_writed_kayboard():
    keyboard = InlineKeyboardMarkup()
    again_btn = InlineKeyboardButton("Вернуться в меню", callback_data=menu_cd.new(action="back"))
    keyboard.add(again_btn)
    return keyboard