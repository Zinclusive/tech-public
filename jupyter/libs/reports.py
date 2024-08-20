import numbers
from copy import copy
from datetime import datetime
from loans import *
import numpy as np
import pandas as pd

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



def statement_report(statement):
    data = []
    for tx in statement.txs:
        if tx.desc:
            data.append([tx.date, tx.desc, tx.amount, tx.bal])
    df = pd.DataFrame(data, columns=['Date', 'Description', 'Amount', 'Balance'])
    return df



def loan_report(customer, expenses, statement : Statement, loan : ILoan, report=None):

    start = statement.txs[0].date
    end = statement.txs[-1].date
    lBal = loan.bal
    lastDate = statement.txs[0].date

    txs = statement.txs.copy()

    data = []
    for tx in txs:
        if tx.desc:
            lBal = getattr(tx, "lBal", lBal)
            iMonth = (tx.date.year - start.year) * 12 + (tx.date.month - start.month)
            data.append([iMonth, tx.date, tx.desc, tx.amount, tx.bal, lBal])
            if lBal < 0.01:
                break
        else:
            pass
    df = pd.DataFrame(data, columns=['iMonth', 'Date', 'Description', 'Amount', 'Balance', "Loan Bal"])
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Amount'] = df['Amount'].apply(lambda x: '{:.2f}'.format(x))
    df['Balance'] = df['Balance'].apply(lambda x: '{:.2f}'.format(x))
    df['Loan Bal'] = df['Loan Bal'].apply(lambda x: '{:.2f}'.format(x))
    return df



