import unittest
from datetime import date

from cstm.representative_helpers import representative_list, representatives_from_transactions
from cstm.dataclasses import Transaction, District
from cstm.enums import TransactionType


class RepresentativeListTestCase(unittest.TestCase):
    """
    This test case is responsible for testing the representative_list method in cstm.representative_helpers
    """

    def test_representatives_terms_in_date_range(self):
        start_dates = [date(2012, 10, 1), date(2013, 2, 19), date(2021, 12, 31)]
        end_dates = [date(2014, 4, 12), date(2020, 4, 20), date(2022, 4, 18)]

        for i in range(len(start_dates)):
            start_date = start_dates[i]
            end_date = end_dates[i]
            representatives = representative_list(start_date, end_date)
            for representative in representatives:
                for year in representative.district_by_year.keys():
                    self.assertTrue(start_date.year <= year <= end_date.year)


class RepresentativesFromTransactionsTestCase(unittest.TestCase):
    """
    This test case is responsible for testing the representatives_from_transactions method in
    cstm.representative_helpers
    """
    transactions = [
        Transaction(1, "Brian Spates", District.from_district_string("MD05"), "Google", "GOOG",
                    TransactionType.PURCHASE, date(2022,4,18), (1001.00, 15000.00), None),
        Transaction(2, "Brian Spates", District.from_district_string("MD05"), "Google", "GOOG",
                    TransactionType.SALE, date(2022, 4, 18), (12000.00, 15000.00), None),
        Transaction(3, "Brian Spates", District.from_district_string("MD05"), "Google", "GOOG",
                    TransactionType.PURCHASE, date(2022, 4, 18), (0.00, 1000000.00), None),
        Transaction(4, "Brian Spates", District.from_district_string("MD05"), "Google", "GOOG",
                    TransactionType.SALE, date(2022, 4, 18), (12.00, 15.00), None),
        Transaction(5, "Brian Spates", District.from_district_string("MD05"), "Google", "GOOG",
                    TransactionType.PURCHASE, date(2022, 4, 18), (1.00, 2.00), None)
    ]

    def test_empty_list_returns_empty(self):
        self.assertEqual([], representatives_from_transactions([]))

    def test_trade_counts_match_samples(self):
        representatives = representatives_from_transactions(self.transactions)
        rep = representatives[0]
        self.assertEqual(rep.trade_count, 5)
        self.assertEqual(rep.purchase_count, 3)
        self.assertEqual(rep.sale_count, 2)

    def test_avg_transaction_value_is_average(self):
        representatives = representatives_from_transactions(self.transactions)
        rep = representatives[0]
        self.assertEqual(rep.avg_transaction_value, 104303.1)

    def test_total_ranges_match_samples(self):
        representatives = representatives_from_transactions(self.transactions)
        rep = representatives[0]
        purchase_range = 1002.00, 1015002.00
        sale_range = 12012.00, 15015.00
        self.assertEqual(sale_range, rep.total_sale_range)
        self.assertEqual(purchase_range, rep.total_purchase_range)
