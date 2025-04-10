# #json #requests #API #datetime #logging #pytest #pandas
import json
from typing import Dict, Any

from src.utils import get_time_for_greeting, get_date_range, PATH_TO_EXCEL, get_slice_of_data, read_data_file


# В Excel-файле такая дата: '10.04.2021 20:30:00'

def main_info(date_time: str) -> Dict[str, Any]:
    """
    Функция, объединяющая логику веб-страницы "Главная".
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS (напр. '2021-04-10 20:30:00').
    Возвращает JSON-ответ со следующими данными: 1) приветствие с указанием текущего времени суток;
    2) информация по каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые
    100 рублей); 3) топ-5 транзакций по сумме платежа; 4) курс валют; 5) стоимость акций из S&P500.
    """
    # Приветствие в зависимости от текущего времени суток
    greeting = get_time_for_greeting()

    # Получение выборки данных из файла
    df = read_data_file()

    # Заготовка данных для вывода
    data = {
        "greeting": greeting,
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": []
    }

    spent_df = df[df["Сумма платежа"] < 0]  # DataFrame только с расходами

    card_grouped = spent_df.groupby(by="Номер карты")  # Группировка данных по номерам карт
    cards_sum = card_grouped["Сумма операции с округлением"].sum().reset_index()  # Расчет сумм расходов по каждой карте

    # Добавление в данные для вывода сводной информации по каждой карте (в т.ч. отдельно для всех неуказанных карт)
    for index, row in cards_sum.iterrows():
        data["cards"].append(
            {
                "last_digits": row["Номер карты"].replace("*", ""),
                "total_spent": round(row["Сумма операции с округлением"], 2),
                "cashback": round(row["Сумма операции с округлением"] * 0.01, 2)
            }
        )

    # Отбор только успешных транзакций для формирования ТОП-5 по сумме
    filter_ok_transactions = df[df["Статус"] == "OK"]
    # Сортировка транзакций по убыванию суммы и выбор первых 5 транзакций по размеру суммы
    sorted_by_sum_df = filter_ok_transactions.sort_values(by="Сумма операции с округлением", ascending=False)
    top_by_sum = sorted_by_sum_df.head(5)

    # Добавление в данные для вывода сводной информации по ТОП-5 транзакциям по сумме операции
    for index, row in top_by_sum.iterrows():
        data["top_transactions"].append(
            {
                "date": row["Дата операции"].split(" ")[0],     # Вывод даты без времени в формате str
                "amount": round(row["Сумма операции с округлением"], 2),
                "category": row["Категория"],
                "description": row["Описание"]
            }
        )

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data


def events_info(date_time) -> Dict[str, Any]:
    """
    Главная функция страницы "События" ....
    """
    # Получение интервала дат для анализа транзакций
    start_date, end_date = get_date_range(date_time)

    # Получение выборки данных за указанный период
    slice_df = get_slice_of_data(PATH_TO_EXCEL, start_date, end_date)

    pass
    # json_data = json.dumps(data, ensure_ascii=False, indent=4)
    # return json_data