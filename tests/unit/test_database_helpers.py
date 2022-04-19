import unittest
from cstm.database_helpers import get_db_connection, get_most_popular_companies, get_most_popular_companies_helper, \
    transaction_query
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


def transaction_empty_request():
    request = Request({})
    request.form = {'member_name': "", 'transaction_year': "", 'company': ""}

    return request


class TransactionQueryTestCase(unittest.TestCase):
    """
    This test case is meant to test the transaction_query method in the Database Helpers file
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

        self.assertEqual(transaction_count, len(transaction_query(transaction_empty_request())))

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
            request = transaction_empty_request()
            request.form['transaction_year'] = year
            self.assertEqual(transaction_counts[year], len(transaction_query(request)))

    def test_empty_request_with_member_all(self):
        request = transaction_empty_request()
        request.form['member_name'] = 'all'
        self.assertEqual(32, len(transaction_query(request)))


def company_empty_request_purchase():
    request = Request({})

    # Empty request includes default transaction_type of "P" for purchase
    request.form = {'company': "", 'ticker': "", 'transaction_type': "P", 'transaction_year': ""}

    return request


def company_request_sale():
    request = Request({})
    request.form = {'company': "", 'ticker': "", 'transaction_type': "S", 'transaction_year': ""}

    return request


class GetMostPopularCompaniesTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_most_popular_companies method in the Database Helpers file.
    """

    def test_empty_request_returns_correct_companies_with_purchase_type(self):
        """
        This test makes sure that an empty request results in the every transaction being returned. Note an empty
        request includes transaction type of purchase.
        """

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE transaction_type = \"P\" GROUP BY company;")
        conn.commit()
        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count, len(get_most_popular_companies(company_empty_request_purchase())))

    def test_sales_type_request_returns_correct_companies(self):
        """
        This test makes sure that a request with transaction type sales results in the correct number of transaction
        being returned.
        """

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE transaction_type = \"S\" GROUP BY company;")
        conn.commit()
        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count, len(get_most_popular_companies(company_request_sale())))

    def test_returns_company_most_transactions_with_type_purchase(self):
        """
        This test makes sure that the company with the most transactions is first when picking transaction
        type purchase.
        """

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE transaction_type = \"P\" GROUP BY company ORDER BY COUNT(id) "
                    "DESC;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][3], get_most_popular_companies(company_empty_request_purchase())[0][1])

    def test_returns_company_most_transactions_with_type_sale(self):
        """
        This test makes sure that the company with the most transactions is first when picking transaction type sale.
        """

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE transaction_type = \"S\" GROUP BY company ORDER BY COUNT(id) "
                    "DESC;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][3], get_most_popular_companies(company_request_sale())[0][1])


class GetMostPopularCompaniesHelperTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_most_popular_companies_helper method in the Database Helpers file.
    """
    def test_empty_request_returns_correct_tuple(self):
        """
        This test makes sure that an empty request results in the correct tuple being returned.
        """

        query_company, query_ticker, query_trans_type, query_transaction_year, select_query_year = \
        get_most_popular_companies_helper(company_empty_request_purchase())

        self.assertEqual(query_transaction_year, "TRUE")
        self.assertEqual(query_company, "AND TRUE")
        self.assertEqual(query_ticker, "AND TRUE")
        self.assertEqual(query_trans_type, "AND transaction_type = \'P\'")
        self.assertEqual(select_query_year, "NULL")

    def test_nonempty_request_returns_correct_tuple(self):
        """
        This test makes sure that a nonempty request results in the correct tuple being returned.
        """

        # Nonempty request
        request = Request({})
        request.form = {'company': "EMC Corporation", 'ticker': "EMC", 'transaction_type': "S",
                        'transaction_year': "2016"}

        query_company, query_ticker, query_trans_type, query_transaction_year, select_query_year = \
            get_most_popular_companies_helper(request)

        self.assertEqual(query_transaction_year, "strftime(\'%Y\',transaction_date) = \'2016\'")
        self.assertEqual(query_company, "AND company = \'EMC Corporation\'")
        self.assertEqual(query_ticker, "AND ticker = \'EMC\'")
        self.assertEqual(query_trans_type, "AND transaction_type = \'S\'")
        self.assertEqual(select_query_year, "strftime(\'%Y\',transaction_date)")