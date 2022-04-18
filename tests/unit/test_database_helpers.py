import unittest
from cstm.database_helpers import get_db_connection, transaction_query, generate_like_condition_string
import sqlite3
from flask import Request


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


class LikeConditionGenerationTestCase(unittest.TestCase):
    def test_empty_variable_name(self):
        self.assertTrue(generate_like_condition_string(variable_name="", partial_value="") == "TRUE")
        self.assertTrue(generate_like_condition_string(variable_name="", partial_value="aa") == "TRUE")

    def test_empty_partial_value(self):
        self.assertTrue(generate_like_condition_string(variable_name="aa", partial_value="") == "TRUE")

    def test_regular_query(self):
        self.assertEqual(generate_like_condition_string(variable_name="aa", partial_value="bb"), "aa like %bb%")
