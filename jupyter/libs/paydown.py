from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from copy import copy

"""
For simplicity, this model assumes the loan payment schedule is the same as the income schedule - a monthly period.
A customer with their loan
On the first of each month, the customer receives a paycheck and then makes a loan payment and pays the expenses.
If the customer gets paid every two weeks, then the calculated equivalent monthly payment = paycheck * 26 / 12.
"""

"""
Loan Class
==========

This module contains the Loan class to model a loan with methods to calculate payments.

Classes
-------
Loan
    A class to represent a loan with methods to calculate payments.
"""

class Loan:
    """
    A class to represent a loan.

    Attributes
    ----------
    bal : float
        The balance of the loan.
    rate : float
        The interest rate of the loan.
    term : int
        The term of the loan in months.
    pmt : float
        The monthly payment of the loan.
    mp_type : int
        The method type for calculating minimum payment.
    xl : float
        The lower threshold for balance.
    xh : float
        The upper threshold for balance.
    r : float
        The percentage rate that when multiplied by the remaining balance will get the minimum balance.
    fees : float
        Any optional additional fees.


    Methods
    -------
    calc_pmt():
        Calculates the monthly payment of the loan using a fixed rate and term.
    calc_min_pmt():
        Calculates the minimum payment of the loan.
    """

    def __init__(self, bal, rate, term, mp_type=2, xl=25, xh=1000, r=0.02, fees=0):
        """
        Constructs all the necessary attributes for the loan object.

        Parameters
        ----------
        bal : float
            The balance of the loan.
        rate : float
            The interest rate of the loan.
        term : int
            The term of the loan in months.
        mp_type : int, optional
            The method type for calculating minimum payment (default is 2).
        xl : float, optional
            The lower threshold for balance (default is 25).
        xh : float, optional
            The upper threshold for balance (default is 1000).
        r : float, optional
            The interest rate for minimum payment calculation (default is 0.02).
        fees : float, optional
            The fees for minimum payment calculation (default is 0).
        """
        self.bal = bal
        self.rate = rate
        self.term = term
        self.pmt = self.calc_pmt()
        self.mp_type = mp_type
        self.xl = xl
        self.xh = xh
        self.r = r
        self.fees = fees

    def calc_pmt(self):
        """
        Calculates the monthly payment of the loan.

        Returns
        -------
        float
            The monthly payment of the loan.
        """
        r = self.rate
        n = self.term
        pmt = (self.bal * r) / (1 - (1 + r) ** -n)
        return pmt

    def calc_min_pmt(self):
        """
        Calculates the minimum payment of the loan.

        Returns
        -------
        float
            The minimum payment of the loan.

        Raises
        ------
        Exception
            If the minimum payment type is invalid.
        """

        def f():
            if self.mp_type == 1:
                return self.r * self.bal

            if self.mp_type == 2:
                if self.bal > self.xh: return self.r * self.bal + self.fees
                if self.bal > self.xl: return self.xl + self.fees
                return self.bal + self.fees

            raise Exception("Invalid option")
        
        # Creditors typically round up to the nearest dollar making it easier for both the creditor and the debtor to handle.
        return round(f() + 0.4999)
        


class Customer:
    """
    A customer with income, expenses, and a balance.
    """
    
    def __init__(self, annual_income = 40000, end_bal = 0):
        """
        Attributes
        ----------
        annual_income : float
            The amount of money the customer makes per year, e.g. $40,000.
        paycheck : float
            The amount of money the customer makes per paycheck, e.g. $1300 after taxes every two weeks for $40,000/year.
        end_bal : float, optional
            The approximate amount of money the customer has in their account at the end of each pay period (default is 0).
        """

        taxes = 0.12
        monthly_income = annual_income * (1 - taxes) / 12

        self.annual_income = annual_income
        self.paycheck = monthly_income
        self.end_bal = end_bal


class Tx:
    """
    Model a transaction, i.e. an amount at some time.
    """
    def __init__(self, date, desc, amount):
        self.date = date
        self.desc = desc
        self.amount = amount
        self.bal = 0 # The new balance after the transaction is applied.


class Statement:
    """
    A balance and a list of transactions that affect the balance.
    By default, we start with no money in the bank.
    """
    def __init__(self, bal = 0):
        self.bal = bal
        self.txs = []
        self.total = {}

    def add_tx(self, tx):
        tx = copy(tx)
        self.bal = self.bal + tx.amount
        tx.bal = self.bal
        self.txs.append(tx)
        t = self.total.get(tx.desc, 0)
        t += tx.amount
        self.total[tx.desc] = t
        



class Period:
    """
    A class to represent a period of time.

    Attributes
    ----------
    start : datetime
        The start date of the period.
    months : int, optional
        The number of months in the period (default is 0).
    days : int, optional
        The number of days in the period (default is 0).
    parts : int, optional
        The number of parts the period is divided into (default is 1).

    Methods
    -------
    __iter__():
        Initializes the iterator.
    __next__():
        Returns the next date in the period.
    """

    def __init__(self, start, months=0, days=0, parts=1):
        """
        Constructs all the necessary attributes for the period object.

        Parameters
        ----------
        start : datetime
            The start date of the period.
        months : int, optional
            The number of months in the period (default is 0).
        days : int, optional
            The number of days in the period (default is 0).
        parts : int, optional
            The number of parts the period is divided into (default is 1).
        """
        self.start = start
        self.months = months
        self.days = days
        self.parts = parts

    def __iter__(self):
        """
        Initializes the iterator.

        Returns
        -------
        datetime
            The start date of the period.
        """
        self._now = self.start
        return self

    def __next__(self):
        """
        Returns the next date in the period.

        Returns
        -------
        datetime
            The next date in the period.

        Raises
        ------
        StopIteration
            If the period has ended.
        """
        r = self._now

        if self.months > 0:
            if self.parts == 1:
                self._now += relativedelta(months=self.months)
            elif self._now.day == 1:
                self._now.day = 15
            else:
                self._now = self._now.replace(day=1) + relativedelta(months=1)
        else:
            self._now += relativedelta(months=self.months)
        return r



class Report:
    """
    A simple report generator with headers and formatted columns.
    EXAMPLE USAGE:
        report = Report("Name:<15", "Balance:>10,.2f")
        print(report.header())
        print(report.row("Fred", 1000))
        print(report.row("Wilma", 2000))
    OUTPUT:
        Name                Balance
        ===============  ==========
        Fred               1,000.00
        Wilma              2,000.00

    """
    def __init__(self, *headers):
        self.headers = headers
        self.names = [h.split(':')[0] for h in headers]
        self.formats = [h.split(':')[1] if ':' in h else f"<{len(h.split(':')[0])}" for h in headers]
        self.names_formats = [h.split(':')[1].split(',')[0].split('.')[0] if ':' in h else f"<{len(h.split(':')[0])}" for h in headers]
        self.colSpacing = '  '
        # print(self.names)
        # print(self.headers)
        # print(self.formats)
        # print(self.names_formats)
    
    def header(self):
        h = ''
        for i, name in enumerate(self.names):
            h += f"{{:{self.names_formats[i]}}}".format(name) + self.colSpacing
        h += '\n'
        for i, name in enumerate(self.names):
            w = int(self.names_formats[i][1:])
            div = '=' * w
            h += f"{div}" + self.colSpacing
        return h
    
    def row(self, *args):
        s = ''
        for i, arg in enumerate(args):
            if not isinstance(arg, (int, float)):
                arg = str(arg)
            w = int(self.names_formats[i][1:])
            field = f"{{:{self.formats[i]}}}".format(arg)
            s += field + self.colSpacing
        return s
        


def run_statement(loan, customer, expenses, periods = 24):
    "Run a statement scenario into the future."
    pmt = loan.pmt
    statement = Statement()    

    # Start on the first day of the next month.
    d = date.today().replace(day=1) + timedelta(days=32)
    d = d.replace(day=1)

    for i in range(periods):
        statement.add_tx(Tx(d, "", 0))
        statement.add_tx(Tx(d, "paycheck", customer.paycheck))
        statement.add_tx(Tx(d, "loan payment", -pmt))
        statement.add_tx(Tx(d, "expenses", -expenses))

        # Next month
        d += relativedelta(months=1)
    return statement


def statement_report(report, customer, expenses, statement, loan):
    """
    EXAMPLE:
      report = Report("Date:<10", "Description:<15", "Amount:>10,.2f", "Balance:>10,.2f", "Amount:>10,.2f", "Balance:>10,.2f")
      customer = Customer(40000)
      loan = Loan(5000, 0.12/12, 360)
      expenses = 2000
      statement_them = run_statement(loan, customer, expenses)
      statement_report(report, customer, expenses, statement, loan)
    """
    print("\n\n\n\n")
    report = Report("Date:<10", "Description:<15", "Balance:>10,.2f", "Amount:>10,.2f")
    statement = run_statement(loan, customer, expenses)
    print(f"""
          
Payment: {loan.pmt:,.2f}

{report.header()}""")
    for tx in statement.txs[:10]:
        if tx.desc:
            print({report.row(tx.date, tx.desc, tx.bal, tx.amount)})
        else:
            print()




# ================================================================================
term = 24 # months

# They offer a 200% loan of $5000 for 24 months.
them = Loan(5000, 2/12, term)

# We offer a 59% loan of $5000 for 24 months.
us = Loan(5000, .59/12, term)

customer = Customer()
loan = Loan(5000, 0.12/12, 360)



report = Report("Date:<10", "Description:<15", "Amount:>10,.2f", "Balance:>10,.2f", "Amount:>10,.2f", "Balance:>10,.2f")
customer = Customer(40000)

# Assume that with their loan, your expenses are your paycheck less their payment. That is, for the first month of your loan, you spend yourself down to zero balance.
expenses = customer.paycheck - them.pmt

# Use the same fixed expenses for both loan scenarios.
statement_them = run_statement(them, customer, expenses)
statement_us = run_statement(us, customer, expenses)

print(f"""
SUMMARY:
  With THEM, your balance goes to zero every month and your total expenses over {term} months.
  With US,   your balance increases over time to finally end up with ${statement_us.bal:,.2f} in your account.

THEM:  APR: {them.rate*1200:>6.2f}%   PMT: ${them.pmt:.2f}   Your monthly expenses: ${expenses:.2f}
  US:  APR: {us.rate*1200  :>6.2f}%   PMT: ${us.pmt:.2f}

                            ----------THEM---------  ----------US----------
{report.header()}""")
for i in range(len(statement_us.txs))[:999]:
    tx_us = statement_us.txs[i]
    tx_them = statement_them.txs[i]
    if tx_us.desc:
        print(report.row(tx_us.date, tx_us.desc, tx_them.amount, tx_them.bal, tx_us.amount, tx_us.bal))
    else:
        print()

print(f"""
Your bank account at the end of the {term} months:
  With their loan:  {statement_them.txs[-1].bal:>10,.2f}
  With   our loan:  {statement_us.txs[-1].bal:>10,.2f}

Your savings:       {statement_us.txs[-1].bal - statement_them.txs[-1].bal:>10,.2f}
""")



