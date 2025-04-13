import json
import logging
import os

import pandas as pd


PATH_TO_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "services.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_high_cashback_categories(df: pd.DataFrame, year: str, month: str) -> str:
    """
    Функция, из раздела "Сервисы" анализирующая, какие категории были наиболее выгодными в заданном месяце для выбора
    в качестве категорий повышенного кешбэка.
    Принимает на вход данные для анализа в формате DataFrame, год и месяц в формате str.
    Возвращает JSON-ответ с анализом, сколько на каждой категории расходов можно заработать кешбэка в указанном
    месяце года.
    """

    if df.empty:  # Если данных нет...
        print("Ошибка. Данные для анализа не обнаружены.")
        return ""
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)  # Преобразование дат в столбце
    # "Дата операции" в формат datetime для выборки за месяц

    # Выборка транзакций за заданный месяц определенного года
    slice_df = df[(df["Дата операции"].dt.month == int(month)) & (df["Дата операции"].dt.year == int(year))]
    logger.debug(f"Сделана выборка транзакций за месяц {month} (год {year}).")

    # DataFrame только с расходами (исключая переводы)
    spent_df = slice_df[(slice_df["Сумма платежа"] < 0) & (slice_df["Категория"] != "Переводы")]

    category_grouped = spent_df.groupby(by="Категория", as_index=False)  # Группировка данных по категориям трат
    category_sum = category_grouped["Сумма операции с округлением"].sum()  # Расчет сумм расходов по каждой категории

    # Сортировка сумм расходов по каждой категории по убыванию
    sorted_category_sum = category_sum.sort_values(by="Сумма операции с округлением", ascending=False,
                                                   ignore_index=True)
    result = {}
    # Формирование данных для вывода сводной информации по каждой категории
    for index, row in sorted_category_sum.iterrows():
        result[row["Категория"]] = round(row["Сумма операции с округлением"] * 0.01, 2)
    logger.debug("Сводная информация о кешбеке по каждой категории успешно получена.")

    return json.dumps(result, indent=4, ensure_ascii=False)
