import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

PATH_TO_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")
PATH_TO_USER_SETTINGS_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")
PATH_TO_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "utils.log")



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_date_range(date_time: str) -> tuple[datetime, datetime]:
    """
    Функция получения периода времени для выборки транзакций (для ее последующего анализа).
    Принимает строку с датой и временем в формате YYYY-MM-DD HH:MM:SS, обозначающей конечную границу выборки
    (начало выборки - первый день заданного месяца).
    Возвращает начальную и конечную даты в виде строки для последующей выборки транзакций.
    """
    end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")  # Конечная граница выборки в формате datetime
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0)  # Начальная граница выборки в формате
    # datetime - первое число указанного месяца

    logger.debug("Определен период времени для выборки транзакций.")

    # Возврат дат начала и конца выборки в формате ГГГГ-ММ-ДД
    return start_date, end_date


def read_data_file() -> DataFrame:
    """
        Функция получения объекта DataFrame с транзакциями из файла для последующего анализа.
        Считывает данные из файла.
        Возвращает датафрейм с транзакциями, отсортированный по убыванию даты.
    """
    df_excel = pd.read_excel(PATH_TO_EXCEL, sheet_name="Отчет по операциям")  # Чтение данных из Excel-файла

    df_excel["Номер карты"] = df_excel["Номер карты"].fillna("Карта не указана")  # В ячейки без номера карты
    # записывается "Карта не указана"
    logger.debug(f"Выполнено чтение файла {PATH_TO_EXCEL}.")

    return df_excel


def get_slice_of_data(start_date: datetime, end_date: datetime) -> DataFrame:
    """
        Функция получения выборки транзакций из Excel-файла для последующего анализа.
        Принимает даты начала и конца выборки в виде объектов datetime.
        Возвращает датафрейм с транзакциями за указанный период, отсортированный по возрастанию даты.
    """

    df = read_data_file()  # Чтение данных из Excel-файла

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)  # Преобразование дат в столбце
    # "Дата операции" в формат datetime для выборки по интервалу дат

    slice_df = df[df["Дата операции"].between(start_date, end_date)]  # Выборка транзакций для заданного
    # промежутка дат
    logger.debug(f"Сделана выборка транзакций в диапазоне дат {start_date} - {end_date}.")


    return slice_df


def get_time_for_greeting() -> str:
    """
    Функция возвращает приветствие в формате «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени (на момент запуска программы).
    """
    user_time_hour = datetime.now().hour  # Получение текущего времени (в часах)
    logger.debug("Формируется приветствие для пользователя.")

    if 5 <= user_time_hour < 12:
        return "Доброе утро!"
    elif 12 <= user_time_hour < 18:
        return "Добрый день!"
    elif 18 <= user_time_hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_summary_card_data(df: DataFrame) -> list[dict]:
    """
    Функция получения сводных данных о расходах по всем картам клиента (в т.ч. отдельно для всех неуказанных карт).
    Принимает данные о транзакциях в формате DataFrame.
    Возвращает список словарей в формате:
    [{
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    }]
    """

    spent_df = df[df["Сумма платежа"] < 0]  # DataFrame только с расходами

    card_grouped = spent_df.groupby(by="Номер карты")  # Группировка данных по номерам карт
    cards_sum = card_grouped["Сумма операции с округлением"].sum().reset_index()  # Расчет сумм расходов по каждой карте

    result = []
    # Формирование данных для вывода сводной информации по каждой карте (в т.ч. отдельно для всех неуказанных карт)
    for index, row in cards_sum.iterrows():
        result.append(
            {
                "last_digits": row["Номер карты"].replace("*", ""),
                "total_spent": round(row["Сумма операции с округлением"], 2),
                "cashback": round(row["Сумма операции с округлением"] * 0.01, 2)
            }
        )
    logger.debug("Сводная информация по каждой карте успешно получена.")

    return result


def top_5_transactions_by_sum(df: DataFrame) -> list[dict]:
    """
    Функция получения ТОП-5 транзакций по величине суммы.
    Принимает данные о транзакциях в формате DataFrame.
    Возвращает список словарей в формате:
    [{
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта."
    }]
    """

    # Отбор только успешных транзакций для формирования ТОП-5 по сумме
    filter_ok_transactions = df[df["Статус"] == "OK"]
    # Сортировка транзакций по убыванию суммы
    sorted_by_sum_df = filter_ok_transactions.sort_values(by="Сумма операции с округлением", ascending=False)
    # Выбор первых 5 транзакций по размеру суммы
    top_by_sum = sorted_by_sum_df.head(5)

    result = []
    # Формирование данных для вывода сводной информации по ТОП-5 транзакциям по сумме операции
    for index, row in top_by_sum.iterrows():
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),  # Вывод даты (без времени) в формате str
                "amount": round(row["Сумма операции с округлением"], 2),
                "category": row["Категория"],
                "description": row["Описание"]
            }
        )
    logger.debug("ТОП-5 транзакций по сумме операции успешно получены.")

    return result


def actual_currencies(base_currency: str = "RUB") -> list[dict]:
    """
    Функция получения актуальных курсов валют (из файла `user_settings.json`).
    Принимает строку с тикером базовой валюты, относительно которой рассчитываются курсы валют из файла
    `user_settings.json` (по умолчанию - "RUB").
    Возвращает список словарей в формате:
    [{
      "currency": "USD",
      "rate": 73.21
    }]
    или пустой список, если не удалось получить курс валют.
    """

    try:
        logger.debug("Чтение данных из JSON-файла...")
        with open(PATH_TO_USER_SETTINGS_JSON, "r") as file:
            currencies = json.load(file)["user_currencies"]  # Извлечение из файла `user_settings.json` тикеров валют
            logger.debug("Данные из JSON-файла успешно получены.")
    except json.JSONDecodeError:
        print("Ошибка декодирования файла.")
        logger.error("Произошла ошибка декодирования файла.")
    except FileNotFoundError:
        print(f"Ошибка! Файл по адресу {PATH_TO_USER_SETTINGS_JSON} не найден.")
        logger.error(f"Ошибка! Файл по адресу {PATH_TO_USER_SETTINGS_JSON} не найден.")

    url = "https://api.apilayer.com/exchangerates_data/latest"  # URL для API-запроса текущих курсов валют
    # Ниже - параметры для запроса (базовая валюта (RUB) и список валют для получения курса относительно базовой,
    # перечисленные через запятую)
    payload = {"symbols": ",".join(currencies), "base": base_currency}

    load_dotenv()  # Для загрузки API-ключа из .env-файла
    api_key = os.getenv("API_KEY_APILAYER")

    headers = {"apikey": api_key}  # Заголовок запроса по API-ключу для авторизации на Exchange Rates Data

    response = requests.get(url, headers=headers, params=payload)  # API-запрос на получение курса валют
    if response.status_code != 200:  # Если запрос неудачный...
        print(f"Неудачная попытка получить курс валют {currencies}. Возможная причина: {response.reason}.")
        logger.error(f"Неудачная попытка получить курсы валют {currencies}. Возможная причина: {response.reason}.")
        return []
    response_json = response.json()  # Преобразование данных в JSON-объект
    logger.debug(f"Курсы валют {currencies} по API-запросу успешно получены. Выполняется обработка данных.")

    result = []

    # Извлечение из ответа от API курса валют относительно базовой валюты (по умолчанию "RUB")
    for key, value in response_json["rates"].items():
        result.append(
            {
                "currency": key,
                "rate": round(1 / value, 2)
            }
        )

    return result


def actual_stocks() -> list[dict]:
    """
    Функция получения актуальной стоимости акций (из файла `user_settings.json`).
    Не имеет параметров.
    Возвращает список словарей в формате:
    [{
      "stock": "AAPL",
      "price": 150.12
    }]
    или пустой список, если не удалось получить курс акций.
    """
    try:
        logger.debug("Чтение данных из JSON-файла...")
        with open(PATH_TO_USER_SETTINGS_JSON, "r") as file:
            symbols = json.load(file)["user_stocks"]  # Извлечение из файла `user_settings.json` тикеров акций
            logger.info("Данные из JSON-файла успешно получены.")
    except json.JSONDecodeError:
        print("Ошибка декодирования файла.")
        logger.error("Произошла ошибка декодирования файла.")
    except FileNotFoundError:
        print(f"Ошибка! Файл по адресу {PATH_TO_USER_SETTINGS_JSON} не найден.")
        logger.error(f"Ошибка! Файл по адресу {PATH_TO_USER_SETTINGS_JSON} не найден.")

    url = "http://api.marketstack.com/v2/eod/latest"  # URL для API-запроса курсов акций (End-of-Day Data)
    # Ниже - параметры для запроса (тикеры акций, перечисленные через запятую)
    payload = {"symbols": ",".join(symbols)}

    load_dotenv()  # Для загрузки API-ключа из .env-файла
    api_key = os.getenv("API_KEY_MARKETSTACK")

    headers = {"access_key": api_key}  # Заголовок запроса по API-ключу для авторизации на Marketstack

    response = requests.get(url, headers=headers, params=payload)  # API-запрос на получение курса акций

    if response.status_code != 200:  # Если запрос неудачный...
        print(f"Неудачная попытка получить курсы акций {symbols}. Возможная причина: {response.reason}.")
        logger.error(f"Неудачная попытка получить курсы акций {symbols}. Возможная причина: {response.reason}.")
        return []
    response_json = response.json()  # Преобразование данных в JSON-объект
    logger.debug(f"Курсы акций {symbols} по API-запросу успешно получены. Выполняется обработка данных.")

    result = []

    # Извлечение из ответа от API курса акций относительно "USD"
    for stock_info in response_json["data"]:
        result.append(
            {
                "stock": stock_info["symbol"],
                "price": stock_info["adj_close"]
            }
        )

    return result

    # sorted_df = filtered_df.sort_values(by="Дата операции")
