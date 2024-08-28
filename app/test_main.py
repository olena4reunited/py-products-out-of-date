import datetime
from unittest.mock import patch

from app.main import outdated_products


def mock_today(date: datetime.date) -> patch:
    class MockDate(datetime.date):
        @classmethod
        def today(cls) -> datetime.date:
            return date
    return patch("datetime.date", MockDate)


mocked_products = [
    {
        "name": "salmon",
        "expiration_date": datetime.date(2022, 2, 10),
        "price": 600
    },
    {
        "name": "chicken",
        "expiration_date": datetime.date(2022, 2, 5),
        "price": 120
    },
    {
        "name": "duck",
        "expiration_date": datetime.date(2022, 2, 1),
        "price": 160
    }
]


def test_some_outdated() -> None:
    with mock_today(datetime.date(2022, 2, 4)):
        result = outdated_products(mocked_products)
    assert result == ["duck"]


def test_all_outdated() -> None:
    with mock_today(datetime.date(2022, 2, 15)):
        result = outdated_products(mocked_products)
    assert result == ["salmon", "chicken", "duck"]


def test_none_outdated() -> None:
    with mock_today(datetime.date(2022, 1, 28)):
        result = outdated_products(mocked_products)
    assert result == []


def test_empty_list() -> None:
    with mock_today(datetime.date(2022, 2, 5)):
        result = outdated_products([])
    assert result == []


def test_date_equals_today() -> None:
    with mock_today(datetime.date(2022, 2, 5)):
        result = outdated_products(
            [
                {
                    "name": "tuna",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 350
                }
            ]
        )
    assert result == []


def test_date_yesterday() -> None:
    with mock_today(datetime.date(2022, 2, 5)):
        result = outdated_products(
            [
                {
                    "name": "milk",
                    "expiration_date": datetime.date(2022, 2, 4),
                    "price": 60
                }
            ]
        )
    assert result == ["milk"]
