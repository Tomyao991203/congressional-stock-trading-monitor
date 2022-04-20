import unittest
from cstm.database_helpers import get_db_connection, transaction_query, generate_string_like_condition, \
    generate_string_equal_condition, generate_select_query
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
        self.assertTrue(generate_string_like_condition(key_name="", partial_string="") == "TRUE")
        self.assertTrue(generate_string_like_condition(key_name="", partial_string="aa") == "TRUE")

    def test_empty_partial_value(self):
        self.assertTrue(generate_string_like_condition(key_name="aa", partial_string="") == "TRUE")

    def test_regular_query(self):
        self.assertEqual(generate_string_like_condition(key_name="aa", partial_string="bb"), "aa like \'%bb%\'")


class EqualConditionGenerationTestCase(unittest.TestCase):
    def test_empty_variable_name(self):
        self.assertTrue(generate_string_equal_condition(key_name="", exact_string="") == "TRUE")
        self.assertTrue(generate_string_equal_condition(key_name="", exact_string="aa") == "TRUE")

    def test_empty_partial_value(self):
        self.assertTrue(generate_string_equal_condition(key_name="aa", exact_string="") == "TRUE")

    def test_regular_query(self):
        self.assertEqual(generate_string_equal_condition(key_name="aa", exact_string="bb"), "aa = \"bb\"")


class SelectQueryGenerationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_key = []
        self.one_key = ["one"]
        self.two_key = ["one", "two"]
        self.table_name = "TABLE"
        # self.empty_table_name = ""
        self.empty_conditions = []
        self.one_condition = ["A = \'B\'"]
        self.two_condition = ["A = \'B\'", "C = \'D\'"]

    def test_no_selected_key(self):
        temp_query = generate_select_query(selected_key=self.empty_key, the_table_name=self.table_name,
                                           where_conditions=self.one_condition)
        select_string = "Select *"
        from_string = " From TABLE"
        where_string = " Where A = \'B\'"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_no_where_conditions(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "Select one"
        from_string = " From TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_no_selected_keys_and_where_conditions(self):
        temp_query = generate_select_query(selected_key=self.empty_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "Select *"
        from_string = " From TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_one_selected_key(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "Select one"
        from_string = " From TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_two_selected_key(self):
        temp_query = generate_select_query(selected_key=self.two_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "Select one, two"
        from_string = " From TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_one_where_condition(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.one_condition)
        select_string = "Select one"
        from_string = " From TABLE"
        where_string = " Where A = \'B\'"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_two_where_condition(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.two_condition)
        select_string = "Select one"
        from_string = " From TABLE"
        where_string = " Where A = \'B\' And C = \'D\'"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)





