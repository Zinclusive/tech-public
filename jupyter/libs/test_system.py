from datetime import datetime
import pytest
from customer import *
from loans import *
from period import *
from reports import *
from systems import *
from tools import *
from zinclusive import Zinclusive


def test_system_1():
    # Loan origination date
    start = datetime(2000, 1, 1)

    pIncome = BiWeeklyPeriod(datetime(2000, 1, 1))
    customer = Customer(annual_income=40000, pIncome=pIncome)
    loan = ZLoan(5000)
    r = pIncome.adjust_monthly(Zinclusive.Apr/12)
    MinPmtFloor = Zinclusive.MinPmtFloor[loan.iBand]

    system = CustomerSystem(start=datetime(2000, 1, 1), end=datetime(2000, 1, 1), loan=loan, customer=customer)
    statement = system.get_statement()
    df = loan_report(loan=loan, customer=customer, expenses=0, statement=statement)
    print(df.to_string())




if __name__ == "__main__":
    #pytest.main(["-k", "test_"])
    import inspect
    tests = inspect.getmembers(__import__(__name__), inspect.isfunction)
    tests = [func for name, func in tests if name.startswith("test_")]
    for test in tests: test()
