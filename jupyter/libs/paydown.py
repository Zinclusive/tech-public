from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from copy import copy
from customer import Customer
from loans import *



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



def run_statement(loan, customer, expenses):
    "Run a statement scenario into the future."
    pmt = loan.calc_pmt(loan.term)
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
expenses = customer.paycheck - them.calc_min_pmt()

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



def merge(*statements):
    "Merge multiple statements into one."
    s = Statement()
    for statement in statements:
        s.txs += statement.txs
        s.total.update(statement.total)
        s.bal = statement.bal
    s.txs.sort(key=lambda tx: tx.date)
    return s

