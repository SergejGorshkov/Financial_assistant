from datetime import datetime

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "Дата операции": ["01.01.2025", "15.01.2025", "01.02.2025", "15.02.2025", "20.02.2025", "22.02.2025"],
            "Сумма платежа": [-1000.0, -2000.0, -1500.0, -500.0, -1200.0, 10000.0],
            "Категория": ["Супермаркеты", "АЗС", "Супермаркеты", "Рестораны", "Переводы", "Аванс"],
            "Сумма операции с округлением": [1000.0, 2000.0, 1500.0, 500.0, 1200.0, 10000.0],
        }
    )


@pytest.fixture
def sample_data_with_cards():
    return pd.DataFrame(
        {
            "Номер карты": ["*5678", "*2222", "*3333", "*5678", "*5998"],
            "Сумма платежа": [-1000, -2000, -1500, -500, 1000],
            "Сумма операции с округлением": [1000, 2000, 1500, 500, 1000],
        }
    )


@pytest.fixture
def test_date():
    return "2023-05-15 14:30:00"


@pytest.fixture
def sample_data_for_top_5_transactions():
    return pd.DataFrame(
        {
            "Дата операции": [
                datetime(2023, 1, 1),
                datetime(2023, 1, 2),
                datetime(2023, 1, 3),
                datetime(2023, 1, 4),
                datetime(2023, 1, 5),
                datetime(2023, 1, 6),
            ],
            "Сумма операции с округлением": [1000, 2000, 3000, 4000, 5000, 6000],
            "Категория": ["АЗС", "Аптеки", "Супермаркеты", "Фастфуд", "Мобильная связь", "Каршеринг"],
            "Описание": ["Описание1", "Описание2", "Описание3", "Описание4", "Описание5", "Описание6"],
            "Статус": ["OK", "OK", "FAILED", "OK", "OK", "OK"],
        }
    )


@pytest.fixture
def sample_data_for_top_5_transactions_failed_status():
    return pd.DataFrame(
        {
            "Дата операции": [
                datetime(2023, 1, 1),
                datetime(2023, 1, 2),
                datetime(2023, 1, 3),
                datetime(2023, 1, 4),
                datetime(2023, 1, 5),
                datetime(2023, 1, 6),
            ],
            "Сумма операции с округлением": [1000, 2000, 3000, 4000, 5000, 6000],
            "Категория": ["АЗС", "Аптеки", "Супермаркеты", "Фастфуд", "Мобильная связь", "Каршеринг"],
            "Описание": ["Описание1", "Описание2", "Описание3", "Описание4", "Описание5", "Описание6"],
            "Статус": ["FAILED", "FAILED", "FAILED", "FAILED", "FAILED", "FAILED"],
        }
    )


@pytest.fixture
def mock_user_settings_for_currencies():
    """Фикстура с тестовыми настройками пользователя для запроса курсов валют"""
    return {"user_currencies": ["USD", "EUR", "GBP"]}


@pytest.fixture
def mock_api_response_for_currencies():
    """Фикстура с тестовым ответом API для запроса курсов валют"""
    return {"rates": {"USD": 0.013, "EUR": 0.011, "GBP": 0.0095}, "base": "RUB", "success": True}


@pytest.fixture
def mock_user_settings_for_stocks():
    """Фикстура с тестовыми настройками пользователя для запроса курсов акций"""
    return {"user_stocks": ["AAPL", "GOOGL", "MSFT"]}


@pytest.fixture
def mock_api_response_for_stocks():
    """Фикстура с тестовым ответом API для запроса курсов акций"""
    return {
        "data": [
            {"symbol": "AAPL", "adj_close": 150.12},
            {"symbol": "GOOGL", "adj_close": 2750.45},
            {"symbol": "MSFT", "adj_close": 305.67},
        ]
    }
