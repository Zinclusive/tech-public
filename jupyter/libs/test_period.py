from datetime import datetime
import pytest
from tools import *
from period import *
from itertools import *



def test_period():
    start = datetime(2000, 1, 1)

    # Get paid every two weeks
    period = Period(start=start, days=14)
    it = iter(period)
    n = next(it)
    assert_equals(datetime(2000, 1, 1), n)
    n = next(it)
    assert_equals(datetime(2000, 1, 15), n)
    n = next(it)
    assert_equals(datetime(2000, 1, 29), n)



def expected_dates(period, dates):
    it = iter(period)
    for i,d in enumerate(dates):
        n = next(it)
        assert_equals(datetime.strptime(d, "%Y-%m-%d"), n, f"Date {i+1} is {n}")


def test_period1():
    # Bi-weekly
    period = BiWeeklyPeriod(datetime(2000, 1, 1))
    expected_dates(period, ["2000-01-01", "2000-01-15", "2000-01-29", "2000-02-12", "2000-02-26", "2000-03-11"])

    # Monthly
    period = MonthlyPeriod(datetime(2000, 1, 1))
    expected_dates(period, ["2000-01-01", "2000-02-01", "2000-03-01", "2000-04-01", "2000-05-01"])

    # Does it wrap around the year?
    period = MonthlyPeriod(datetime(2000, 12, 1))
    expected_dates(period, ["2000-12-01", "2001-01-01", "2001-02-01"])

    # Semi-monthly
    period = SemiMonthlyPeriod(datetime(2000, 1, 1), days=[7, 22])
    expected_dates(period, ["2000-01-07", "2000-01-22", "2000-02-07", "2000-02-22", "2000-03-07"])

    # Semi-monthly
    period = SemiMonthlyPeriod(datetime(2000, 1, 1), days=[1, 15])
    expected_dates(period, ["2000-01-01", "2000-01-15", "2000-02-01", "2000-02-15", "2000-03-01"])

    # Semi-monthly - delayed start
    period = SemiMonthlyPeriod(datetime(2000, 1, 8), days=[1, 15])
    expected_dates(period, ["2000-01-15", "2000-02-01", "2000-02-15", "2000-03-01"])


if __name__ == "__main__":
    #pytest.main(["-k", "test_"])
    import inspect
    tests = inspect.getmembers(__import__(__name__), inspect.isfunction)
    tests = [func for name, func in tests if name.startswith("test_")]
    for test in tests: test()
