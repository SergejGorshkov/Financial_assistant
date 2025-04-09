from datetime import datetime
import os

import pandas as pd
from pandas import DataFrame

PATH_TO_EXCEL = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx")

# "2025.04.10 20:30:00"

def get_time_for_greeting() -> str:
    """
    Функция возвращает приветствие в формате «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени (на момент запуска программы).
    """
    user_time_hour = datetime.now().hour
    if 5 <= user_time_hour < 12:
        return "Доброе утро!"
    elif 12 <= user_time_hour < 18:
        return "Добрый день!"
    elif 18 <= user_time_hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


# '2025.04.10 20:30:00'
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

    # Возврат дат начала и конца выборки с их преобразованием в строку в формате ДД.ММ.ГГГГ
    return start_date, end_date



#date_start '2025.04.01 00:00:00'
#date_end '2025.04.10 20:30:00'
def get_slice_of_data(file_path: str, start_date: datetime, end_date: datetime) -> DataFrame:
    """
        Функция получения выборки транзакций из Excel-файла для последующего анализа.
        Принимает строку с путем к файлу с данными о транзакциях, даты начала и конца выборки в виде объектов datetime.
        Возвращает датафрейм с транзакциями за указанный период, отсортированный по возрастанию даты.
    """
    df = pd.read_excel(file_path, sheet_name="Отчет по операциям")  # Чтение данных из Excel-файла
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)  # Создание DF с датами транзакций
    print(df["Дата операции"])  # Для тестирования
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]  # Здесь предварительно
    # нужно привести формат дат к одному виду.Разобраться с кодом. Сделать по-своему
    print(filtered_df)
    # sorted_df = filtered_df.sort_values(by="Дата операции")
    return  # sorted_df


