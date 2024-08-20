import numbers
from copy import copy
from datetime import datetime
from loans import *


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
            if isinstance(arg, datetime):
                arg = arg.strftime('%Y-%m-%d')
            elif not isinstance(arg, numbers.Number):
                arg = str(arg)
            w = int(self.names_formats[i][1:])
            field = f"{{:{self.formats[i]}}}".format(arg)
            s += field + self.colSpacing
        return s



def merge(*statements):
    "Merge multiple statements into one."
    s = Statement()
    for statement in statements:
        s.txs += statement.txs
        s.total.update(statement.total)
        s.bal = statement.bal
    s.txs.sort(key=lambda tx: tx.date)
    return s



def statement_report(customer, expenses, statement, loan, report=None):
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

    report = report or Report("Date:<10", "Description:<15", "Amount:>10,.2f", "Balance:>10,.2f")
    print(f"""


{report.header()}""")
    for tx in statement.txs[:10]:
        if tx.desc:
            print(report.row(tx.date, tx.desc, tx.amount, tx.bal))
        else:
            print()



def loan_report(customer, expenses, statement : Statement, loan : ILoan, report=None):
    """
    """
    print("\n\n\n\n")

    lBal = loan.bal
    lastDate = statement.txs[0].date

    txs = statement.txs.copy()

    report = report or Report("Date:<10", "Description:<15", "Amount:>10,.2f", "Balance:>10,.2f", "LoanBal:>10,.2f")
    print(f"""


{report.header()}""")
    for tx in txs:
        if tx.desc:
            lBal = getattr(tx, "lBal", lBal)
            print(report.row(tx.date, tx.desc, tx.amount, tx.bal, lBal))
        else:
            print()



