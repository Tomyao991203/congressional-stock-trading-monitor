import unittest
from datetime import date
import sqlite3
from flask import Request

from cstm.database_helpers import check_companies_advanced_search, get_db_connection, get_transactions_between, \
    get_companies_btwn_years, get_companies_advanced_search, check_transactions_advanced_search, \
    get_transactions_advanced_search, table_name, \
    convert_db_transactions_to_dataclass, get_companies_advanced_search_helper, generate_string_like_condition, \
    equal_condition, generate_select_query, generate_year_equal_condition, get_transactions_btwn_years


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
        self.assertTrue(equal_condition(expression="", exact_value="") == "TRUE")
        self.assertTrue(equal_condition(expression="", exact_value="aa") == "TRUE")

    def test_empty_partial_value(self):
        self.assertTrue(equal_condition(expression="aa", exact_value="") == "TRUE")

    def test_regular_query(self):
        self.assertEqual(equal_condition(expression="aa", exact_value="bb"), "aa = \'bb\'")


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
        select_string = "SELECT *"
        from_string = " FROM TABLE"
        where_string = " WHERE (A = \'B\')"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_no_where_conditions(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "SELECT one"
        from_string = " FROM TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_no_selected_keys_and_where_conditions(self):
        temp_query = generate_select_query(selected_key=self.empty_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "SELECT *"
        from_string = " FROM TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_one_selected_key(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "SELECT one"
        from_string = " FROM TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_two_selected_key(self):
        temp_query = generate_select_query(selected_key=self.two_key, the_table_name=self.table_name,
                                           where_conditions=self.empty_conditions)
        select_string = "SELECT one, two"
        from_string = " FROM TABLE"
        where_string = ""
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_one_where_condition(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.one_condition)
        select_string = "SELECT one"
        from_string = " FROM TABLE"
        where_string = " WHERE (A = \'B\')"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)

    def test_two_where_condition(self):
        temp_query = generate_select_query(selected_key=self.one_key, the_table_name=self.table_name,
                                           where_conditions=self.two_condition)
        select_string = "SELECT one"
        from_string = " FROM TABLE"
        where_string = " WHERE (A = \'B\' AND C = \'D\')"
        full_query = select_string + from_string + where_string
        self.assertEqual(temp_query, full_query)


class YearEqualConditionGenerationTestCase(unittest.TestCase):
    def test_empty_variable_name(self):
        self.assertTrue(generate_year_equal_condition(key_name="", exact_year="") == "TRUE")
        self.assertTrue(generate_year_equal_condition(key_name="", exact_year="2014") == "TRUE")

    def test_empty_partial_value(self):
        self.assertTrue(generate_year_equal_condition(key_name="aa", exact_year="") == "TRUE")

    def test_regular_query(self):
        self.assertEqual(generate_year_equal_condition(key_name="aa", exact_year="2014"),
                         "strftime(\'%Y\', aa) = \'2014\'")


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
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        connection.commit()
        db_transactions = cursor.fetchall()
        transactions = convert_db_transactions_to_dataclass(db_transactions)
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


def company_empty_request():
    request = Request({})
    request.form = {'company': "", 'ticker': "", 'transCount': "", 'memberCount': "", 'purchaselb': "",
                    'purchaseub': "", 'salelb': "", 'saleub': ""}

    return request


def company_request():
    request = Request({})
    request.form = {'company': "Tesla, Inc", 'ticker': "TSLA", 'transCount': "1", 'memberCount': "1",
                    'purchaselb': "1000001", 'purchaseub': "5000000", 'salelb': "0", 'saleub': "0"}

    return request


class GetCompaniesAdvancedSearchTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_companies_advanced_search method in the Database Helpers file.
    """

    def test_empty_advanced_search_correct_return_string(self):
        """
        This test makes sure that an empty request results in the correct string being returned.
        """
        output_string = " WHERE (TRUE AND TRUE AND TRUE AND TRUE AND TRUE AND TRUE) " \
                        "GROUP BY company HAVING (TRUE AND TRUE)"

        self.assertEqual(get_companies_advanced_search(company_empty_request()), output_string)
    
    def test_nonempty_advanced_search_correct_return_string(self):
        """
        This test makes sure that a nonempty request results in the correct string being returned.
        """
        output_string = " WHERE (company = \'Tesla, Inc\' AND ticker = \'TSLA\' " \
                        "AND purchase_lb >= 1000001 AND purchase_ub <= 5000000 AND sale_lb >= 0 AND sale_ub <= 0) " \
                        "GROUP BY company HAVING (num_transactions = 1 AND num_members = 1)"

        self.assertEqual(get_companies_advanced_search(company_request()), output_string)


class GetCompaniesAdvancedSearchHelperTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_companies_advanced_search_helper method in the Database Helpers file.
    """

    def test_empty_request_returns_correct_tuple(self):
        """
        This test makes sure that an empty request results in the correct tuple being returned.
        """
        query_company, query_ticker, query_transaction_count, query_member_count, query_purchaselb, query_purchaseub, \
            query_salelb, query_saleub = get_companies_advanced_search_helper(company_empty_request())

        self.assertEqual(query_company, "TRUE")
        self.assertEqual(query_ticker, "TRUE")
        self.assertEqual(query_transaction_count, "TRUE")
        self.assertEqual(query_member_count, "TRUE")
        self.assertEqual(query_purchaselb, "TRUE")
        self.assertEqual(query_purchaseub, "TRUE")
        self.assertEqual(query_salelb, "TRUE")
        self.assertEqual(query_saleub, "TRUE")

    def test_nonempty_request_returns_correct_tuple(self):
        """
        This test makes sure that a nonempty request results in the correct tuple being returned.
        """
        query_company, query_ticker, query_transaction_count, query_member_count, query_purchaselb, query_purchaseub, \
            query_salelb, query_saleub = get_companies_advanced_search_helper(company_request())

        self.assertEqual(query_company, "company = \'Tesla, Inc\'")
        self.assertEqual(query_ticker, "ticker = \'TSLA\'")
        self.assertEqual(query_transaction_count, "num_transactions = 1")
        self.assertEqual(query_member_count, "num_members = 1")
        self.assertEqual(query_purchaselb, "purchase_lb >= 1000001")
        self.assertEqual(query_purchaseub, "purchase_ub <= 5000000")
        self.assertEqual(query_salelb, "sale_lb >= 0")
        self.assertEqual(query_saleub, "sale_ub <= 0")


class GetCompaniesBtwnYearsTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_companies_btwn_years method in the Database Helpers file.
    """
    def test_get_request_returns_correct_num_companies(self):
        """
        This test makes sure that a request results in the every transaction being returned. Note a request will
        include a start and end date.
        """
        start_date = date(2015, 3, 10)
        end_date = date(2018, 2, 6)

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM all_transaction "
                    f"WHERE transaction_date BETWEEN '{start_date.isoformat()}' AND '{end_date.isoformat()}' "
                    f"GROUP BY company;")
        conn.commit()
        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count, len(get_companies_btwn_years("GET", company_empty_request(),
                                                                         start_date, end_date)))

    def test_get_request_returns_correct_lowerbound_purchases(self):
        """
        Tests if the lowerbound of purchases for a company is correct.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(value_lb) FROM all_transaction "
                    "WHERE transaction_type = \"P\" AND company = \"Apple Inc.\" GROUP BY company;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][0],
                         get_companies_btwn_years("GET", company_empty_request(),
                                                  date(2013, 7, 11), date(2022, 4, 21))[2][4])

    def test_get_request_returns_correct_upperbound_purchases(self):
        """
        Tests if the upperbound of purchases for a company is correct.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(value_ub) FROM all_transaction "
                    "WHERE transaction_type = \"P\" AND company = \"Apple Inc.\" GROUP BY company;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][0],
                         get_companies_btwn_years("GET", company_empty_request(),
                                                  date(2013, 7, 11), date(2022, 4, 21))[2][5])

    def test_get_request_returns_correct_lowerbound_sales(self):
        """
        Tests if the lowerbound of sales for a company is correct.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(value_lb) FROM all_transaction "
                    "WHERE transaction_type = \"S\" AND company = \"Apple Inc.\" GROUP BY company;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][0],
                         get_companies_btwn_years("GET", company_empty_request(),
                                                  date(2013, 7, 11), date(2022, 4, 21))[2][6])

    def test_get_request_returns_correct_upperbound_sales(self):
        """
        Tests if the upperbound of sales for a company is correct.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(value_ub) FROM all_transaction "
                    "WHERE transaction_type = \"S\" AND company = \"Apple Inc.\" GROUP BY company;")
        conn.commit()

        self.assertEqual(cur.fetchall()[0][0],
                         get_companies_btwn_years("GET", company_empty_request(),
                                                  date(2013, 7, 11), date(2022, 4, 21))[2][7])

    def test_put_request_returns_correct_count_transactions(self):
        """
        Tests if the put request returns the correct number of transactions.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE company = \'Tesla, Inc\' AND ticker = \'TSLA\' "
                    "GROUP BY company HAVING count(id) = 1 AND count(DISTINCT member_name) = 1")
        conn.commit()

        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count,
                         len(get_companies_btwn_years("PUT", company_request(), date(2022, 1, 1), date(2022, 4, 21))))


class CheckCompaniesAdvancedSearchTestCase(unittest.TestCase):
    """
    This test case is meant to test the check_advanced_search method in the Database Helpers file.
    """
    def test_empty_request_returns_false(self):
        """
        This test makes sure that an empty request results in the function returning false.
        """
        self.assertEqual(check_companies_advanced_search(company_empty_request()), False)

    def test_nonempty_request_returns_true(self):
        """
        This test makes sure that a nonempty request results in the function returning true.
        """
        self.assertEqual(check_companies_advanced_search(company_request()), True)


def transaction2_empty_request():
    request = Request({})
    request.form = {'member_name': "", 'distrNum': "", 'company': "", 'ticker': "",
                    'lowerBound': "", 'upperBound': "", 'transType': ""}

    return request


def transaction2_request():
    request = Request({})
    request.form = {'member_name': "Nancy Pelosi", 'distrNum': "CA12", 'company': "Tesla, Inc", 'ticker': "TSLA",
                    'lowerBound': "1000001", 'upperBound': "5000000", 'transType': "P"}

    return request


class GetTransactionsBtwnYearsTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_transactions_btwn_years method in the Database Helpers file.
    """

    def test_get_request_returns_correct_num_transactions(self):
        """
        This test makes sure that a request results in the every transaction being returned. Note a request will
        include a start and end date.
        """
        start_date = date(2015, 3, 10)
        end_date = date(2018, 2, 6)

        # Determine how many entries are in the database:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM all_transaction "
                    f"WHERE transaction_date BETWEEN '{start_date.isoformat()}' AND '{end_date.isoformat()}' ")
        conn.commit()
        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count, len(get_transactions_btwn_years("GET", transaction2_empty_request(),
                                                                            start_date, end_date)))

    def test_put_request_returns_correct_count_transactions(self):
        """
        Tests if the put request returns the correct number of transactions.
        Currently the database is only populated with a representative data subset. This test should be updated
        when the database is updated.
        """

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM all_transaction WHERE member_name = \'Nancy Pelosi\' "
                    "AND state_district_number = \'CA12\' AND company = \'Tesla, Inc\' AND ticker = \'TSLA\' "
                    "AND value_lb >= 1000001 AND value_ub <= 5000000 AND transaction_type = \'P\' GROUP BY company")
        conn.commit()

        transaction_count = len(cur.fetchall())

        self.assertEqual(transaction_count,
                         len(get_companies_btwn_years("PUT", transaction2_request(),
                                                      date(2022, 1, 1), date(2022, 4, 21))))


class GetTransactionsAdvancedSearchTestCase(unittest.TestCase):
    """
    This test case is meant to test the get_transactions_advanced_search method in the Database Helpers file.
    """

    def test_empty_request_returns_correct_tuple(self):
        """
        This test makes sure that an empty request results in the correct array being returned.
        """
        [query_member_name, query_member_district, query_company, query_ticker, query_lb, query_ub, query_trans_type] \
            = get_transactions_advanced_search(transaction2_empty_request())

        self.assertEqual(query_member_name, "TRUE")
        self.assertEqual(query_member_district, "TRUE")
        self.assertEqual(query_company, "TRUE")
        self.assertEqual(query_ticker, "TRUE")
        self.assertEqual(query_lb, "TRUE")
        self.assertEqual(query_ub, "TRUE")
        self.assertEqual(query_trans_type, "TRUE")

    def test_nonempty_request_returns_correct_tuple(self):
        """
        This test makes sure that a nonempty request results in the correct array being returned.
        """
        [query_member_name, query_member_district, query_company, query_ticker, query_lb, query_ub, query_trans_type] \
            = get_transactions_advanced_search(transaction2_request())

        self.assertEqual(query_member_name, "member_name = \'Nancy Pelosi\'")
        self.assertEqual(query_member_district, "state_district_number = \'CA12\'")
        self.assertEqual(query_company, "company = \'Tesla, Inc\'")
        self.assertEqual(query_ticker, "ticker = \'TSLA\'")
        self.assertEqual(query_lb, "value_lb >= 1000001")
        self.assertEqual(query_ub, "value_ub <= 5000000")
        self.assertEqual(query_trans_type, "transaction_type = \'P\'")


class CheckTransactionsAdvancedSearchTestCase(unittest.TestCase):
    """
    This test case is meant to test the check_advanced_search method in the Database Helpers file.
    """
    def test_empty_request_returns_false(self):
        """
        This test makes sure that an empty request results in the function returning false.
        """
        self.assertEqual(check_transactions_advanced_search(transaction2_empty_request()), False)

    def test_nonempty_request_returns_true(self):
        """
        This test makes sure that a nonempty request results in the function returning true.
        """
        self.assertEqual(check_transactions_advanced_search(transaction2_request()), True)
