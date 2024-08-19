from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta


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

    Methods
    -------
    __iter__():
        Initializes the iterator.
    __next__():
        Returns the next date in the period.
    """

    def __init__(self, start=None, months=1, days=[1]):
        """
        Constructs all the necessary attributes for the period object.

        Parameters
        ----------
        start : datetime
            The start date of the period. Default is today.
        months : int, optional
            The number of months in the period (default is 1 for monthly).
        days : int or list, optional
            The number of days (int) in the period (default is [1]).
            Else the days in the month (list) to pay, e.g. [1, 15] means semi-monthly on the 1st and 15th.

        Examples
        --------
        from datetime import date
        from period import Period

        start = date.today()
        period = Period()  # Bi-weekly starting today.
        period = Period(start, days=14)  # Bi-weekly.
        period = Period(start, days=7)  # Weekly.
        period = Period(start, months=1)  # Monthly period on the first of each month.
        period = Period(start, days=[7, 22])  # Semi-monthly period on the 7th and 22nd of each month.
        period = Period(start, months=1, days=[1, 15]) # Semi-monthly period on the 1st and 15th of each month.
        """
        if not start:
            start = date.today()
        self._start = start
        self._type = ""
        if type(days) == int:
            # An integer days means skip that number of days and ignore the months.
            months = 0
        if months:
            if months == 1:
                self._type = "monthly"
            elif months == 6:
                self._type = "semi-annually"
            if days:
                if type(days) == list:
                    if not len(days):
                        raise ValueError("At least one day is required.")
                elif type(days) == int:
                    self._type = "monthly"
                    days = [days]
            else:
                days = [1] # Paid on the first of each month

        elif type(days) == int:
            if days == 7:
                self._type = "weekly"
            elif days == 14:
                self._type = "bi-weekly"
        elif type(days) == list:
            if not months:
                months = 1
            if len(days) == 1:
                self._type = "monthly"
            elif len(days) == 2:
                self._type = "semi-monthly"

        self._months = months
        self._days = days

    def generator(self):
        """
        Returns the generator for the period.
        """
        now = self._start
        if self._months:
            if not self._days or type(self._days) != list:
                raise ValueError("Expected a list of days for monthly period.")
            if self._months == 1:
                i = next((index for index, day in enumerate(self._days) if day <= self._start.day), 0)

                while True:
                    count = 0
                    while now.day != self._days[i]:
                        now += relativedelta(days=1)
                        count += 1
                        if (count > 365):
                            raise ValueError("Invalid day for monthly period.")
                    i = (i+1) % len(self._days)
                    yield now
                    now += relativedelta(days=1)
        elif type(self._days) == int and self._days > 0:
            yield now
            while True:
                now += relativedelta(days=self._days)
                yield now
        else:
            raise ValueError("Invalid period.")

    def __iter__(self):
        return iter(self.generator())


    def num_periods(self, months=12):
        """
        Returns the number of periods in the given number of months.
        """
        end = self._start + relativedelta(months=months)
        return len([x for x in self if x < end])

class MonthlyPeriod(Period):
    """
    A class to represent a monthly period of time.
    """
    def __init__(self, start):
        super().__init__(start, months=1)


class SemiMonthlyPeriod(Period):
    """
    A class to represent a semi-monthly period of time.
    """
    def __init__(self, start, days=[1, 15]):
        super().__init__(start, months=1, days=days)


class BiWeeklyPeriod(Period):
    """
    A class to represent a bi-weekly period of time.
    """
    def __init__(self, start):
        super().__init__(start, days=14)



