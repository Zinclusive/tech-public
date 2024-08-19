from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from paydown import Statement


class ISystem:
    """
    Interface for system classes.
    A "system" is anything that begins with an initial condition and evolves over time.
    EXAMPLE:
        system = CustomerSystem(...)
        for state in system:
            print(state)
    """
    def __init__(self):
        pass




class CustomerSystem(ISystem):
    """
    A system that models a customer with a periodic fixed income, getting a loan, and paying it down over time.
    """
    def __init__(self, start, end, loan, customer, pIncome):
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
        self._pIncome = pIncome
        self.paycheck = customer.paycheck


    def __iter__(self):
        """
        Initialize the iterator.
        """
        pmt = 123.45
        statement = Statement()


        # ADD PERIODIC INCOME, LOAN PAYMENTS, AND EXPENSES
        # Start on the first day of the next month.
        d = date.today().replace(day=1) + timedelta(days=32)
        d = d.replace(day=1)

        d = self._start
        for d in self._pIncome:
            statement.add_tx(Tx(d, "", 0))
            statement.add_tx(Tx(d, "paycheck", self.paycheck))
            statement.add_tx(Tx(d, "loan payment", -pmt))
            statement.add_tx(Tx(d, "expenses", -expenses))

            # Next month
            d += relativedelta(months=1)
        while d < self._end:
            statement.add_tx(Tx(d, "", 0))
            statement.add_tx(Tx(d, "paycheck", self._customer.paycheck))


            statement.add_tx(Tx(d, "loan payment", -pmt))
            statement.add_tx(Tx(d, "expenses", -expenses))

            # Next month
            d += relativedelta(months=1)
        for i in range(periods):
            statement.add_tx(Tx(d, "", 0))
            statement.add_tx(Tx(d, "paycheck", customer.paycheck))
            statement.add_tx(Tx(d, "loan payment", -pmt))
            statement.add_tx(Tx(d, "expenses", -expenses))

            # Next month
            d += relativedelta(months=1)




