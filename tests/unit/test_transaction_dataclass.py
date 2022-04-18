import unittest
import random
from cstm.dataclasses import Transaction, District, State
from datetime import date

class TransactionAverageValueTestCase(unittest.TestCase):

    def test_average_value_between_bounds(self):
        transaction = Transaction(0, "", District(State.MARYLAND, 1), "", "", "",
                                  date(2022, 1, 1), (1001.00, 15000.00), "")
        for _ in range(20):
            n1, n2 = random.randrange(0, 10000000), random.randrange(0, 10000000)
            transaction.value_range = (min(n1, n2), max(n1, n2))
            self.assertTrue(transaction.value_range[0] < transaction.get_average_value() < transaction.value_range[1])

    def test_average_value_range_midpoint(self):
        transaction = Transaction(0, "", District(State.MARYLAND, 1), "", "", "",
                                  date(2022, 1, 1), (1001.00, 15000.00), "")
        for _ in range(20):
            n1, n2 = random.randrange(0, 10000000), random.randrange(0, 10000000)
            transaction.value_range = (min(n1, n2), max(n1, n2))
            self.assertEqual(transaction.get_average_value(), (n1 + n2) / 2)
