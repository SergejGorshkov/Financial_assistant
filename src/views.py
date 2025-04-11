import json

from src.utils import get_time_for_greeting, get_date_range, PATH_TO_EXCEL, get_slice_of_data, read_data_file, \
    get_summary_card_data, top_5_transactions_by_sum, actual_currencies, actual_stocks


def main_info(date_time: str) -> str:
    """
    Функция, объединяющая логику веб-страницы "Главная".
    Принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS (напр. '2021-04-10 20:30:00').
    Возвращает JSON-ответ со следующими данными: 1) приветствие с указанием текущего времени суток;
    2) информация по каждой карте (последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые
    100 рублей); 3) топ-5 транзакций по сумме платежа; 4) курс валют (по умолчанию относительно "RUB");
    5) стоимость акций (End-of-Day Data) из S&P500.
    """

    # Получение интервала дат для анализа транзакций
    start_date, end_date = get_date_range(date_time)

    # Получение выборки данных за указанный период
    df = get_slice_of_data(start_date, end_date)

    data = {
        "greeting": get_time_for_greeting(),  # Приветствие в зависимости от текущего времени суток
        "cards": get_summary_card_data(df),   # Сводная информации по каждой карте
        "top_transactions": top_5_transactions_by_sum(df),  # Сводная информации по ТОП-5 транзакциям по сумме операции
        # "currency_rates": actual_currencies(),  # Информация по текущим курсам валют (из `user_settings.json`)
        "stock_prices": actual_stocks()  # Информация по курсам (End-of-Day Data) акций (из `user_settings.json`)
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data
