from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from customer import *
from loans import *
from reports import *
from tx import Tx




class ISystem:
    """
    A "system" is anything that begins with an initial condition and evolves over time, such as a loan or statement.
    EXAMPLE:
        system = CustomerSystem(...)
        for state in system:
            print(state)
    """
    def __init__(self):
        pass

    def get_statement(self):
        raise NotImplementedError("get_statement() must be implemented in a derived class.")




class CustomerSystem(ISystem):
    """
    A system that models a customer with a periodic fixed income, getting a loan, and paying it down over time.
    """
    def __init__(self, start : date, end : date, loan : ILoan, customer : Customer):
        """
        Initialize a new instance of the class.
        Parameters:
        - start (date): The start date of the simulation.
        - end (date): The end date of the simulation.
        - loan (ILoan): The loan to be paid down.
        - customer (Customer): The borrower.
        - pIncome (Period): The fixed income period, e.g. monthly, bi-weekly.
        """
        super().__init__()

        self._start = start
        self._end = end
        self._loan = loan
        self._customer = customer
        self.paycheck = customer.paycheck

    @property
    def customer(self): return self._customer
    @property
    def loan(self): return self._loan
    @property
    def pIncome(self): return self.customer.pIncome

    def get_statement(self):
        """
        Initialize the iterator.
        """
        statement = Statement()

        # Estimated monthly expenses
        expenses = 2803.33

        bal = self.loan.bal
        apr = Zinclusive.Apr
        r = self.pIncome.adjust_monthly(apr/12)

        # ADD PERIODIC INCOME, LOAN PAYMENTS, AND EXPENSES
        d = self._start
        end = self._start + relativedelta(years=3)

        statement.add_tx(Tx(d, key="apr", value=apr))
        statement.add_tx(Tx(d, desc=f"APR={apr:.2f}%", key="apr", value=apr))
        statement.add_tx(Tx(d, key="r", value=r))
        iPayment = 0

        tx = Tx(d)
        tx.lBal = bal

        for d in self.pIncome:
            if d > end: break

            # We cannot require a payment before 10 days after the loan starts.
            days = (d - self._start).days
            if days >= 10:
                MinPmtFloor = Zinclusive.MinPmtFloor[self.loan.iBand]
                MinPmtPctPrin = Zinclusive.MinPmtPctPrin[self.loan.iBand]
                MinPmtPctPrin = self.pIncome.adjust_monthly(MinPmtPctPrin/100)
                MinPmtPrin = bal*MinPmtPctPrin
                pmt = min(bal * (1+r/100), max(MinPmtPrin, MinPmtFloor))

                statement.add_tx(Tx(d, "", 0))
                statement.add_tx(Tx(d, "paycheck", self.paycheck))
                tx = Tx(d, "loan payment", -pmt)
                bal = bal*(1+r/100) - pmt
                tx.lBal = bal
                statement.add_tx(tx)
                statement.add_tx(Tx(d, "expenses", -expenses))
                iPayment += 1

                if iPayment >= Zinclusive.AprDropsOn:
                    apr = Zinclusive.AprDropsTo
                    r = self.pIncome.adjust_monthly(apr/12)
                    statement.add_tx(Tx(d, desc=f"APR={apr:.2f}%", key="apr", value=apr))
                    statement.add_tx(Tx(d, key="r", value=r))

            # Next month
            d += relativedelta(months=1)

        return statement




