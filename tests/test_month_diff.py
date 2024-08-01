
import pytest
import datetime
from src.utils.month_diff import month_diff
def test_month_diff():
    date1 = datetime.datetime(2023, 1, 1)
    date2 = datetime.datetime(2024, 1, 1)
    date3 = datetime.datetime(2024, 7, 1)

    assert month_diff(date1, date2) == 12
    assert month_diff(date1, date3) == 18
    assert month_diff(date2, date3) == 6
    assert month_diff(date3, date2) == -6  # data3 está depois de data2

