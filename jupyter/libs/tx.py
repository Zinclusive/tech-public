class Tx:
    """
    Model a transaction, i.e. an amount at some time.
    """
    def __init__(self, date, desc='', amount=0, key=None, value=None):
        self.date = date
        self.desc = desc
        self.amount = amount
        self.key = key # The name of an event, e.g. "rate".
        self.value = value # The value of the event, e.g. 0.12.
        self.bal = 0 # The new balance after the transaction is applied.

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.desc:
            return f"{self.date.strftime('%Y-%m-%d')} {self.amount:>8.2f} {self.bal:>8.2f} {self.desc}"
        return ""


