from zinclusive import Zinclusive
from paydown import Tx


class ILoan:
    """
    Common interface for all loans.
    """

    def __init__(self, bal):
        self.bal = bal
        self.iBand = next((i for i, band in enumerate(Zinclusive.bands) if i+1 < len(Zinclusive.bands) and band[i] <= self.bal <= band[i+1]), None)
        if self.iBand is None:
            raise Exception("Invalid balance. Does not fit in a band.")
        self.band = self.iBand + 1

    def calc_pmt(self, period):
        """
        Calculates the monthly payment of the loan.

        Returns
        -------
        float
            The monthly payment of the loan.
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def payments(self):
        """
        Returns an iterator for the loan payments.

        Returns
        -------
        iterator
            An iterator for the loan payments.
        """
        raise NotImplementedError


class ZLoan(ILoan):
    """
    A loan that is part of the Zinclusive product.
    """
    def __init__(self, bal):
        self.bal = bal
        self.iBand = next((i for i, band in enumerate(Zinclusive.bands) if i+1 < len(Zinclusive.bands) and band[i] <= self.bal <= band[i+1]), None)
        if self.iBand is None:
            raise Exception("Invalid balance. Does not fit in a band.")
        self.band = self.iBand + 1

    def payments(self, period):
        """
        Returns an iterator of Tx objects for the loan payments.

        Parameters
        ----------
        period : Period
            The period for the payments. Typically the same as the income period plus an optional days in the future.
        """


        payment = self.calc_pmt()

    class ZLoanIterator:
        def __init__(self, loan):
            self.loan = loan
            self.i = 0

        def generator():


        def __next__(self):
            if self.i < len(Zinclusive.bands[self.loan.iBand]):
                self.i += 1
                return Zinclusive.bands[self.loan.iBand][self.i]
            raise StopIteration

    def __iter__(self):
        return ZLoanIterator(self)


    def calc_pmt(self, period):
        pass

    def calc_min_pmt(self):
        pass




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

class Loan(ILoan):
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

    def __init__(self, bal, rate, term=0, mp_type=2, xl=25, xh=1000, r=0.02, fees=0):
        """
        Constructs all the necessary attributes for the loan object.

        Parameters
        ----------
        bal : float
            The balance of the loan.
        rate : float
            The interest rate of the loan.
        term : int
            The term of the loan in months. 0 = infinite (default is 0).
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
        self.mp_type = mp_type
        self.xl = xl
        self.xh = xh
        self.r = r
        self.fees = fees

    def calc_pmt(self, period):
        """
        Calculates the monthly payment of the loan.

        Returns
        -------
        float
            The monthly payment of the loan.
        """
        if self.term <= 0: raise Exception("Term must be greater than 0 to call this method.")
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
