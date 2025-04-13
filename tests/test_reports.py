import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, mock_open

from src.reports import write_result_to_file, spending_by_category


# Тесты для декоратора write_result_to_file
def test_write_result_to_file_success():
    """Тест успешного выполнения функции с декоратором"""

    @write_result_to_file("report_from_spending_by_category.txt")
    def some_function():
        return "Вызвана функция some_function (успешно). \nРезультат: \nКакой-то результат."

    with patch("builtins.open", mock_open()) as mock_file:
        result = some_function()
        assert result == "Вызвана функция some_function (успешно). \nРезультат: \nКакой-то результат."
        # mock_file.assert_called_once()


def test_write_result_to_file_failure():
    """Тест обработки ошибки в декорируемой функции"""

    @write_result_to_file("report_from_spending_by_category.txt")
    def some_function():
        raise ValueError("Вызвана функция 'some_function' (неуспешно). Ошибка: какая-то ошибка.")

    with patch("builtins.open", mock_open()) as mock_file:
        result = some_function()
        assert result is None
        # mock_file.write.assert_called_once()


transactions = pd.DataFrame({
        "Дата операции": ["01.01.2025", "15.01.2025", "01.02.2025", "15.02.2025", "20.02.2025", "22.02.2025"],
        "Сумма платежа": [-1000.0, -2000.0, -1500.0, -500.0, -1200.0, 10000.0],
        "Категория": ["Супермаркеты", "АЗС", "Супермаркеты", "Рестораны", "Переводы", "Аванс"],
        "Сумма операции с округлением": [1000.0, 2000.0, 1500.0, 500.0, 1200.0, 10000.0]
    })

# Тесты для функции spending_by_category
@pytest.mark.parametrize("transactions, category, start_date, expected", [(transactions, "АЗС", "25.01.2025", {
        "Дата операции": [datetime(2025, 1, 15)],
        "Сумма платежа": [-2000.0],
        "Категория": ["АЗС"],
        "Сумма операции с округлением": [2000.0]}),
        (transactions, "Супермаркеты", "15.02.2025", {
        "Дата операции": [datetime(2025, 1, 1), datetime(2025, 2, 1)],
        "Сумма платежа": [-1000.0, -1500.0],
        "Категория": ["Супермаркеты", "Супермаркеты"],
        "Сумма операции с округлением": [1000.0, 1500.0]})
])
def test_spending_by_category_success(transactions, category, start_date, expected):
    """Тест базовой функциональности"""
    result = spending_by_category(transactions, category, start_date)
    assert result.to_dict(orient='list') == expected
