from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from copy import copy
from customer import Customer
from loans import *
from tx import Tx
from reports import *




def run_statement(loan : Loan, customer : Customer, expenses):
    "Run a statement scenario into the future."
    #pmt = loan.calc_pmt()
    statement = Statement()

    # Start on the first day of the next month.
    # d = date.today().replace(day=1) + timedelta(days=32)
    # d = d.replace(day=1)


    # for i in range(periods):
    #     statement.add_tx(Tx(d, "", 0))
    #     statement.add_tx(Tx(d, "paycheck", customer.paycheck))
    #     statement.add_tx(Tx(d, "loan payment", -pmt))
    #     statement.add_tx(Tx(d, "expenses", -expenses))

    #     # Next month
    #     d += relativedelta(months=1)
    return statement


def scenario():
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




