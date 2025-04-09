# #json #requests #API #datetime #logging #pytest #pandas
import json
from typing import Dict, Any

from src.utils import get_time_for_greeting, get_date_range, PATH_TO_EXCEL, get_slice_of_data


# В Excel-файле такая дата: '10.04.2025 20:30:00'

def main_info(date_time: str) -> Dict[str, Any]:
    """
    Функция, объединяющая логику веб-страницы "Главная".
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS (напр. '2025.04.10 20:30:00').
    Возвращает JSON-ответ со следующими данными: 1) приветствие с указанием текущего времени суток;
    2) информация по каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые
    100 рублей); 3) топ-5 транзакций по сумме платежа; 4) курс валют; 5) стоимость акций из S&P500.
    """
    # 1. Приветствие
    greeting = get_time_for_greeting()

    # Получение интервала дат для анализа транзакций
    start_date, end_date = get_date_range(date_time)

    # Получение выборки данных за указанный период
    sorted_df = get_slice_of_data(PATH_TO_EXCEL, start_date, end_date)


    # Подготовка данных к выводу...
    data = {
        "greeting": greeting
    }
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    # print(start_date, end_date)  # Для тестирования
    return json_data