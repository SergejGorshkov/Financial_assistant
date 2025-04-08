from datetime import datetime

import pandas as pd

PATH_TO_EXCEL = "./data/operations.xlsx"

# "2018-05-20 15:00"    см использование TimesTemp???

def get_correct_dates(date_time: str):
    """
    return '01.05.2018 15:00:00', '20.05.2018 15:00:00'
    """
    end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    start_date = end_date.replace(day=1)  # Здесь д.б. 2 аргумента (что-то менять - на что-то)

    return start_date, end_date



#date_start '01.05.2018 15:00'
#date_end '20.05.2018 15:00'
def get_period(file_path: str, date_start: str, date_end: str):
    """
        Функция получения периода
    """
    df = pd.read_excel(file_path, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[(df["Дата операции"] >= date_start) & (df["Дата операции"] <= date_end)]
    sorted_df = filtered_df.sort_values(by="Дата операции")
    return  sorted_df


def get_time_greating():
    user_time_hour = datetime.now().hour
    if 5 <= user_time_hour < 12:
        return "Доброе утро!"
    elif 12 <= user_time_hour < 18:
        return "Добрый день!"
    elif 18 <= user_time_hour < 23:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"
