class Customer:
    """
    A customer with periodic income and expenses.
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


    def paycheck(self, period):
        if period.type == "monthly":
            return self.monthly_income
        if period.type == "semi-monthly":
            return self.monthly_income/2
        if period.type == "weekly":
            return self.annual_income / 52
        if period.type == "bi-weekly":
            return self.annual_income / 26
        raise Exception("Invalid period type")

    def pay_period_expenses(self, loan, period):
        return self.paycheck - loan.bal * loan.rate / 12