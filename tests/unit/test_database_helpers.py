import unittest
from datetime import date
import sqlite3
from flask import Request


import cstm.database_helpers
from cstm.database_helpers import get_db_connection, transaction_query, get_transactions_between


class DBConnectTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_db_connection method in the Database Helpers file
    """

    def test_get_connection_empty_string_is_valid(self):
        self.assertTrue(isinstance(get_db_connection(""), sqlite3.Connection))

    def test_get_connection_no_arg(self):
        columns = ["id", "member_name", "state_district_number", "company", "ticker", "transaction_type",
                   "transaction_date", "value_lb", "value_ub", "description", "link"]
        connection = get_db_connection()
        self.assertTrue(isinstance(connection, sqlite3.Connection))
        cursor = connection.execute("select * from all_transaction")
        for name in list(map(lambda x: x[0], cursor.description)):
            self.assertTrue(name in columns)


def empty_request():
    request = Request({})
    request.form = {'member_name': "", 'transaction_year': "", 'company': ""}

    return request


class TransactionQueryTestCase(unittest.TestCase):
    """
    This test case is meant to test the transaction_query method in the Database Heleprs file
    Currently the database is only populated with a representative data subset. Any tests that rely on this
        (starting with "test_sample_database_") should be updated when the full database is in place
    """

    def test_empty_request_returns_all(self):
        """
        This test makes sure that an empty request results in the every transaction being returned.
        """
        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("select * from all_transaction")
        conn.commit()
        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count, len(transaction_query(empty_request())))

    def test_sample_database_correct_years(self):
        """
        This test makes a query for each year in the database, ensuring that the number of
        transactions returned match up with the sample database transactions
        """
        transaction_counts = {
            2013: 1,
            2014: 12,
            2015: 11,
            2016: 4,
            2017: 2,
            2018: 1,
            2019: 0,
            2020: 0,
            2021: 0,
            2022: 1
        }

        for year in transaction_counts.keys():
            request = empty_request()
            request.form['transaction_year'] = year
            self.assertEqual(transaction_counts[year], len(transaction_query(request)))

    def test_empty_request_with_member_all(self):
        request = empty_request()
        request.form['member_name'] = 'all'
        self.assertEqual(32, len(transaction_query(request)))


class TransactionsBetweenTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_transactions_between method in cstm.database_helpers
    """

    def test_all_transactions_in_range(self):
        start_dates = [date(2012, 1, 1), date(2013, 1, 4), date(2021, 12, 31)]
        end_dates = [date(2014, 4, 12), date(2020, 4, 20), date(2022, 4, 18)]
        for i in range(len(start_dates)):
            start_date = start_dates[i]
            end_date = end_dates[i]
            transactions = get_transactions_between(start_date, end_date)
            for t in transactions:
                self.assertTrue(start_date <= t.date <= end_date)

    def test_flipped_range_returns_empty_list(self):
        start_dates = [date(2012, 1, 1), date(2013, 1, 4), date(2021, 12, 31)]
        end_dates = [date(2014, 4, 12), date(2020, 4, 20), date(2022, 4, 18)]
        for i in range(len(start_dates)):
            self.assertEqual([], get_transactions_between(end_dates[i], start_dates[i]))


class ConvertDBTransactionTestCase(unittest.TestCase):
    """
    This test case is meant to test the convert_db_transactions_to_dataclass method in
    cstm.database_helpers
    """

    def test_convert_transactions_from_db(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {cstm.database_helpers.table_name} LIMIT 100")
        connection.commit()
        db_transactions = cursor.fetchall()
        transactions = cstm.database_helpers.convert_db_transactions_to_dataclass(db_transactions)
        for i in range(len(transactions)):
            db_t = db_transactions[i]
            t = transactions[i]
            self.assertEqual(t.id, db_t["id"])
            self.assertEqual(t.member_name, db_t["member_name"])
            self.assertEqual(str(t.member_district), db_t["state_district_number"])
            self.assertEqual(t.company, db_t["company"])
            self.assertEqual(t.ticker, db_t["ticker"])
            self.assertEqual(str(t.type), "Purchase" if db_t["transaction_type"] == "P" else "Sale")
            self.assertEqual(t.date.isoformat(), db_t["transaction_date"])
            self.assertEqual(t.value_range[0], db_t["value_lb"])
            self.assertEqual(t.value_range[1], db_t["value_ub"])
            self.assertEqual(t.description, None if db_t["description"] == "None" else db_t["description"])
