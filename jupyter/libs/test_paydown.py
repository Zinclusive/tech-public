from datetime import datetime
import pytest
from jupyter.libs.Customer import Customer
from tools import *
from paydown import *
from loans import *

def test_loan_pmt():
    "Sanity check that the standard 30-year mortgage payment is correct."
    loan = Loan(100000, 0.12/12, 360)
    assert(round(loan.pmt, 2) == 1028.61)


def test_loan_min_pmt_1():
    loan = Loan(100000, 0.12/12, 360, mp_type=1)

    loan.bal = 2000
    mp = loan.calc_min_pmt()
    assert_equals(40.00, round(mp, 2))

    loan.bal = 1000
    mp = loan.calc_min_pmt()
    assert_equals(20.00, round(mp, 2))

    loan.bal = 26
    mp = loan.calc_min_pmt()
    assert_equals(1.00, round(mp, 2))

    loan.bal = 999.99
    mp = loan.calc_min_pmt()
    assert_equals(20.00, round(mp, 2))

    loan.bal = 25
    mp = loan.calc_min_pmt()
    assert_equals(1, round(mp, 2))


def test_loan_min_pmt_2():
    bal=2000
    rate=0.12/12
    xl=25
    xh=1000
    r=0.02
    fees=0
    loan = Loan(bal=bal, rate=rate, term=25, mp_type=2, xl=xl, xh=xh, r=r, fees=fees)

    loan.bal = 2000
    mp = loan.calc_min_pmt()
    assert_equals(40.00, round(mp, 2), "Percentage of balance plus fees")

    loan.bal = 1000
    mp = loan.calc_min_pmt()
    assert_equals(25.00, round(mp, 2), "Min fixed payment")

    loan.bal = 999.99
    mp = loan.calc_min_pmt()
    assert_equals(25.00, round(mp, 2), "Min fixed payment")

    loan.bal = 25
    mp = loan.calc_min_pmt()
    assert_equals(25.00, round(mp, 2), "A small balance becomes the payment")

    loan.bal = 10
    mp = loan.calc_min_pmt()
    assert_equals(10.00, round(mp, 2), "A small balance becomes the payment")


def test_period():
    start = datetime(2000, 1, 1)

    # Get paid every two weeks
    period = Period(start=start, days=14)
    n = iter(period)
    n = next(period)
    assert_equals(datetime(2000, 1, 15), n)
    n = next(period)
    assert_equals(datetime(2000, 1, 29), n)



def expected_dates(period, dates):
    n = iter(period)
    for i,d in enumerate(dates):
        n = next(period)
        assert_equals(datetime.strptime(d, "%Y-%m-%d"), n, f"Date {i+1} is {n}")


def test_period1():
    # Bi-weekly
    period = BiWeeklyPeriod(datetime(2000, 1, 1))
    expected_dates(period, ["2000-01-15", "2000-01-29", "2000-02-12", "2000-02-26", "2000-03-11"])

    # Monthly
    period = MonthlyPeriod(datetime(2000, 1, 1))
    expected_dates(period, ["2000-02-01", "2000-03-01", "2000-04-01", "2000-05-01"])

    # Does it wrap around the year?
    period = MonthlyPeriod(datetime(2000, 12, 1))
    expected_dates(period, ["2001-01-01", "2001-02-01"])

    # Semi-monthly
    period = SemiMonthlyPeriod(datetime(2000, 1, 1))
    expected_dates(period, ["2000-01-15", "2000-02-01", "2000-02-15", "2000-03-01"])


def test_periods():
    "Multiple periods merged together"

    # Customer makes $40K per year and lives paycheck to paycheck.
    customer = Customer(annual_income=40000, end_bal=0)

    # Our loan's origination date.
    orig = datetime(2000, 1, 25)

    # Customer gets paid bi-weekly
    pIncome = Period(orig, days=14)

    # Customer pays them every month on the first.
    paymentThem = Period(orig, months=1)

    # Customer pays us after each paycheck.
    paymentUs = Period(orig, days=14)

    # They offer a 200% loan of $5000.
    them = Loan(5000, 2/12)

    # We offer a 59% loan of $5000.
    us = Loan(5000, .59/12)

    # The customer's expenses are whatever is left after paying the loan.
    expenses = customer.pay_period_expenses(them, paymentThem)

    sThem = run_statement(loan=them, customer=customer, expenses=expenses)
    sUs = run_statement(customer=customer, us=us, them=them, pIncome=pIncome, pPayment=paymentThem)


def test_payment():
    term = 24
    loan = Loan(100000, 12/12)
    period = Period(datetime(2000, 1, 1), months=1)
    n = period.num_periods(months=term)
    assert_equals(24, n)


def test_spreadsheet_payment_band1():
    with pytest.raises(Exception) as e:
        loan = ZLoan(100000)

if __name__ == "__main__":
    pytest.main([__file__])