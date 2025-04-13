import json
from datetime import datetime
from unittest.mock import patch, mock_open

import pandas as pd
import pytest

from src.utils import get_date_range, read_data_file, get_slice_of_data, get_time_for_greeting, get_summary_card_data, \
    top_5_transactions_by_sum, actual_currencies, actual_stocks


def test_get_date_range_success(test_date):
    """Тест на успешное выполнение функции"""
    expected_start_date = datetime(2023, 5, 1, 0, 0, 0)
    expected_end_date = datetime(2023, 5, 15, 14, 30, 0)

    start_date, end_date = get_date_range(test_date)

    assert start_date == expected_start_date
    assert end_date == expected_end_date


##################################################################################################

def test_read_data_file_success():
    """Тест успешного чтения файла"""
    # Создаем тестовый DataFrame
    test_data = {
        "Номер карты": ["*5456", None],
        "Дата операции": ["01.01.2023", "15.01.2023"],
        "Сумма платежа": [-1000, -2000],
        "Категория": ["Супермаркеты", "АЗС"]
    }
    mock_df = pd.DataFrame(test_data)

    # Мокаем pd.read_excel
    with patch('pandas.read_excel', return_value=mock_df) as mock_read:
        result = read_data_file()

        # Проверяем вызовы
        mock_read.assert_called_once_with(
            "C:\\Users\\17\\Desktop\\Projects\\Financial_assistant\\data\\operations.xlsx",
            sheet_name="Отчет по операциям")

        # Проверяем результат
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert list(result.columns) == ["Номер карты", "Дата операции", "Сумма платежа", "Категория"]
        # Проверяем обработку пустых значений в номере карты
        assert result["Номер карты"].iloc[1] == "Карта не указана"


def test_read_data_file_empty():
    """Тест с пустым файлом"""
    # Мокаем pd.read_excel для возврата пустого DataFrame
    with patch('pandas.read_excel', return_value=pd.DataFrame()):
        result = read_data_file()

        # Проверяем результат
        assert isinstance(result, pd.DataFrame)
        assert result.empty


##################################################################################################
def test_get_slice_of_data_success(sample_dataframe):
    """Тест на успешную работу функции"""
    with patch('src.utils.read_data_file', return_value=sample_dataframe):
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 31)

        result = get_slice_of_data(start_date, end_date)

        assert len(result) == 2
        assert all(result["Дата операции"].dt.date >= start_date.date())
        assert all(result["Дата операции"].dt.date <= end_date.date())


def test_get_slice_of_data_empty_result(sample_dataframe):
    """Тест случая, когда нет данных в указанном диапазоне"""
    with patch('src.utils.read_data_file', return_value=sample_dataframe):
        start_date = datetime(2025, 10, 1)
        end_date = datetime(2025, 12, 30)

        result = get_slice_of_data(start_date, end_date)

        assert len(result) == 0


def test_get_slice_of_data_empty_input():
    """Тест на случай чтения пустого файла"""
    with patch('src.utils.read_data_file', return_value=pd.DataFrame()):
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 30)

        result = get_slice_of_data(start_date, end_date)

        assert len(result) == 0


###############################################################################################
@pytest.mark.parametrize("hour, expected_greeting", [
    (4, "Доброй ночи!"),
    (5, "Доброе утро!"),
    (11, "Доброе утро!"),
    (12, "Добрый день!"),
    (17, "Добрый день!"),
    (18, "Добрый вечер!"),
    (22, "Добрый вечер!"),
    (23, "Доброй ночи!"),
    (0, "Доброй ночи!"),
])
def test_get_time_for_greeting(hour, expected_greeting):
    """Тест всех временных диапазонов с параметризацией"""
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, hour)
        assert get_time_for_greeting() == expected_greeting


###############################################################################################
def test_get_summary_card_data_success(sample_data_with_cards):
    """Тест на успешную работу функции"""
    result = get_summary_card_data(sample_data_with_cards)

    # Проверка структуры результата
    assert isinstance(result, list)
    assert len(result) == 3  # 3 уникальных карты

    # Проверка данных по картам
    expected = [
        {"last_digits": "2222", "total_spent": 2000.0, "cashback": 20.0},
        {"last_digits": "3333", "total_spent": 1500.0, "cashback": 15.0},
        {"last_digits": "5678", "total_spent": 1500.0, "cashback": 15.0}
    ]

    assert result == expected


def test_get_summary_card_data_with_empty_dataframe():
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame()
    result = get_summary_card_data(empty_df)
    assert result == []


###############################################################################################
def test_top_5_transactions_by_sum_success(sample_data_for_top_5_transactions):
    """Тест на успешную работу функции"""
    # with patch('your_module.logger.debug') as mock_logger:
    result = top_5_transactions_by_sum(sample_data_for_top_5_transactions)

    # Проверка структуры результата
    assert isinstance(result, list)
    assert len(result) == 5  # Должно вернуть 5 транзакций

    # Проверка, что не включены FAILED-транзакции
    assert all(transaction["category"] != "Супермаркеты" for transaction in result)


def test_top_5_transactions_by_sum_with_empty_dataframe():
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame()
    result = top_5_transactions_by_sum(empty_df)
    assert result == []


def test_top_5_transactions_by_sum_with_failed_status(sample_data_for_top_5_transactions_failed_status):
    """Тест, если нет успешных транзакций"""
    assert top_5_transactions_by_sum(sample_data_for_top_5_transactions_failed_status) == []


###############################################################################################

def test_actual_currencies_successful(mock_user_settings_for_currencies, mock_api_response_for_currencies):
    """Тест успешного получения курсов валют"""
    # Мокаем файл с настройками
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_user_settings_for_currencies))):
        # Мокаем API-запрос
        with patch("requests.get") as mock_get:
            # Настраиваем мок ответа
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response_for_currencies

            # Вызываем тестируемую функцию
            result = actual_currencies()

            # Проверяем результаты
            assert len(result) == 3
            assert result[0]["currency"] == "USD"
            assert result[0]["rate"] == round(1 / 0.013, 2)
            assert result[1]["currency"] == "EUR"
            assert result[1]["rate"] == round(1 / 0.011, 2)
            assert result[2]["currency"] == "GBP"
            assert result[2]["rate"] == round(1 / 0.0095, 2)


def test_actual_currencies_if_file_not_found():
    """Тест случая, когда файл настроек `user_settings.json` не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = actual_currencies()
        assert result == []


def test_actual_currencies_if_invalid_json():
    """Тест случая с неправильным JSON"""
    with patch("builtins.open", mock_open(read_data="Ошибка декодирования файла.")):
        result = actual_currencies()
        assert result == []


###############################################################################################

def test_actual_stocks_successful(mock_user_settings_for_stocks, mock_api_response_for_stocks):
    """Тест успешного получения курсов акций"""
    # Мокаем файл с настройками
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_user_settings_for_stocks))):
        # Мокаем API-запрос
        with patch("requests.get") as mock_get:
            # Настраиваем мок ответа
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response_for_stocks

            # Вызываем тестируемую функцию
            result = actual_stocks()

            # Проверяем результаты
            assert len(result) == 3
            assert result[0]["stock"] == "AAPL"
            assert result[0]["price"] == 150.12
            assert result[1]["stock"] == "GOOGL"
            assert result[1]["price"] == 2750.45
            assert result[2]["stock"] == "MSFT"
            assert result[2]["price"] == 305.67


def test_actual_stocks_if_file_not_found():
    """Тест случая, когда файл настроек `user_settings.json` не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = actual_stocks()
        assert result == []


def test_actual_stocks_if_invalid_json():
    """Тест случая с неправильным JSON"""
    with patch("builtins.open", mock_open(read_data="Ошибка декодирования файла.")):
        result = actual_stocks()
        assert result == []
