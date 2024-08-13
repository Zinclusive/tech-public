from datetime import datetime
import pytest
from tools import *
from paydown import *


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
    

def period_test():
    start = datetime(2000, 1, 1)

    # Get paid every two weeks
    period = Period(start=start, days=14)
    n = next(period)
    assert_equals(datetime(2000, 1, 1), n)



if __name__ == "__main__":
    pytest.main(["-k", "test_"])