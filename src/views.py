import json
import logging
import os

from src.utils import (actual_currencies,
                       actual_stocks,
                       get_date_range,
                       get_slice_of_data,
                       get_summary_card_data,
                       get_time_for_greeting,
                       top_5_transactions_by_sum)

PATH_TO_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "views.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_info(date_time: str) -> str:
    """
    Функция, объединяющая логику веб-страницы "Главная".
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS (напр. '2021-04-10 20:30:00').
    Возвращает JSON-ответ со следующими данными: 1) приветствие с указанием текущего времени суток;
    2) информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые
    100 рублей); 3) топ-5 транзакций по сумме платежа; 4) курс валют (по умолчанию относительно "RUB");
    5) стоимость акций (End-of-Day Data) из S&P500.
    """

    logger.debug("Вызвана функция 'main_info' страницы 'Главная'.")

    # Получение интервала дат для анализа транзакций
    start_date, end_date = get_date_range(date_time)
    logger.info("Определен период времени для выборки транзакций.")

    # Получение выборки данных за указанный период
    df = get_slice_of_data(start_date, end_date)
    logger.info(f"Сделана выборка транзакций в диапазоне дат {start_date} - {end_date}.")

    data = {
        "greeting": get_time_for_greeting(),  # Приветствие в зависимости от текущего времени суток
        "cards": get_summary_card_data(df),  # Сводная информации по каждой карте
        "top_transactions": top_5_transactions_by_sum(df),  # Сводная информации по ТОП-5 транзакциям по сумме операции
        "currency_rates": actual_currencies(),  # Информация по текущим курсам валют (из `user_settings.json`)
        "stock_prices": actual_stocks()  # Информация по курсам (End-of-Day Data) акций (из `user_settings.json`)
    }
    logger.info(f"Получена обобщенная информация по финансовым операциям в диапазоне дат {start_date} - {end_date}.")

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data
