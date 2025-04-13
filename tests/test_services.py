import json

import pandas as pd
import pytest

from src.services import get_high_cashback_categories


@pytest.mark.parametrize(
    "year, month, expected",
    [
        ("2025", "01", {"АЗС": 20.0, "Супермаркеты": 10.0}),
        ("2025", "02", {"Рестораны": 5.0, "Супермаркеты": 15.0}),
    ],
)
def test_get_high_cashback_categories_success(sample_dataframe, year, month, expected):
    """Тест на корректную работу функции"""
    result = get_high_cashback_categories(sample_dataframe, year, month)
    assert json.loads(result) == expected


def test_get_high_cashback_categories_with_empty_dataframe():
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame()
    result = get_high_cashback_categories(empty_df, "2025", "01")
    assert result == ""
