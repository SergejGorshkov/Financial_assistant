import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

PATH_TO_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(PATH_TO_LOG_FILE, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def write_result_to_file(filename: str = "") -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Декоратор, который автоматически записывает в файл результат выполнения декорируемых функций.
    Декоратор имеет необязательный входной параметр 'filename' - имя файла, в который вносится информация
    о работе функции. Если при вызове декоратора параметр 'filename' не указан, логирование выводится в файл
    `reports_result.txt`, находящийся в папке 'logs'."""

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = function(*args, **kwargs)
                logging_info = f"Вызвана функция '{function.__name__}' (успешно). \nРезультат: \n{result}"
            except Exception as error_info:
                logging_info = (
                    f"Вызвана функция '{function.__name__}' (неуспешно). Ошибка: {error_info}."
                )
                result = None
            # Если передано имя файла для записи результата, определяется путь к нему и записывается результат
            if filename:
                path_to_logfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", filename)
                with open(path_to_logfile, "w", encoding="UTF-8") as file:
                    file.write(f"{logging_info}\n")
            else:
                path_to_logfile = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                               f"logs/report_from_{function.__name__}.txt")
                with open(path_to_logfile, "w", encoding="UTF-8") as file:
                    file.write(f"{logging_info}\n")
            return result

        return wrapper

    return decorator


@write_result_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str,
                         start_date: Optional[str | datetime] = None) -> pd.DataFrame:
    """
    Функция, выбирающая из данных о транзакциях траты по заданной категории.
    Принимает данные о транзакциях в формате DataFrame, название категории в формате str, опционально дату
    в формате str (ДД.ММ.ГГГГ). Если дата не передана, то берется текущая дата.
    Возвращает траты по заданной категории за последние три месяца (от переданной или текущей даты) в DataFrame.
    """

    if start_date is None:  # Если дата для анализа выборки не передана, то принимается текущая дата
        start_date = datetime.now()
        end_date = start_date - timedelta(days=90)
    else:
        start_date = datetime.strptime(start_date, '%d.%m.%Y')
        end_date = start_date - timedelta(days=90)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)  # Преобразование дат
    # в столбце "Дата операции" в формат datetime для выборки по интервалу дат

    slice_df = transactions[transactions["Дата операции"].between(end_date, start_date)]  # Выборка транзакций для
    # заданного промежутка дат
    logger.debug(
        f"Сделана выборка транзакций в диапазоне дат {end_date.strftime('%d.%m.%Y')} - {start_date.strftime(
            '%d.%m.%Y')}.")

    # DataFrame только с расходами (включая переводы)
    spent_df = slice_df[slice_df["Сумма платежа"] < 0]

    # Поиск строк, в которых значение в столбце "Категория" соответствует целевой категории
    result = spent_df[spent_df["Категория"] == category]
    logger.debug(f"Данные по тратам в категории '{category}' за последние три месяца успешно получены.")

    return result
