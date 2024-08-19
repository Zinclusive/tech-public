import numpy as np

class Zinclusive:
    """
    This file contains the parameters for the Zinclusive loan product.
    """

    # Suffixes:
    #  BW = Bi-weekly
    #  SM = Semi-monthly



    # Starting Annual Percentage Rate (APR) for the loan
    Apr = 59.975

    # Later Annual Percentage Rate (APR) for the loan if the customer makes consistent good payments
    AprDropsTo = 35.950

    # The month that the APR drops if the borrower makes consistent good payments
    AprDropsOn = 13

    # The minimum amount that we lend.
    MinInitBal = 1000

    # Band: a number in range 1..4
    # iBand: a number in range 0..3 = Band-1
    # If balance is 500, then iBand = -1 and is not allowed since we don't lend less than 1000
    # If balance is 2500, then iBand = 1
    bands = [1000, 2000, 4000, 7000, 10000]

    # Monthly minimum percentage of the principle to calculate the payment
    MinPmtPctPrin = np.array([5.5, 5.5, 5.25, 4.5])
    MinPmtPctPrinBW = MinPmtPctPrin*12/26
    MinPmtPctPrinSM = MinPmtPctPrin/2

    # The minimum payment for a monthly term
    MinPmtFloor = np.array([120, 125, 130, 150])
    MinPmtFloorBW = MinPmtFloor*12/26
    MinPmtFloorSM = MinPmtFloor*2


