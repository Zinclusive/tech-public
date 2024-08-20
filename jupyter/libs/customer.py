from period import Period

class Customer:
    """
    A customer with periodic income and expenses.
    """

    def __init__(self, annual_income = 40000, pIncome : Period = None):
        """
        Attributes
        ----------
        annual_income : float
            The amount of money the customer makes per year, e.g. $40,000.
        pIncome : Period
            The payment period that the customer receives income, e.g. bi-weekly.
        """

        taxes = 0.12
        monthly_income = annual_income * (1 - taxes) / 12

        self.annual_income = annual_income
        self.paycheck = monthly_income
        self.pIncome = pIncome
