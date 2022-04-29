from operator import truediv
import sqlite3
from flask import Request
from datetime import date
from typing import List, Union

from cstm.enums import TransactionType
from cstm.dataclasses import Transaction, District
from cstm.query import value_between, value_greater_equal, value_less_equal, equal_condition, aggregating_conditions

db_file_path = r"database/database.db"
table_name = r"all_transaction"


def get_db_connection(db_file: str = db_file_path):
    """
    Get the database connection
    :param db_file: Database file path
    :return: SQL3 Database Connection for the given file
    """
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def generate_string_like_condition(key_name: str, partial_string: str) -> str:
    """
    return a like condition for string(SQLite)
    :param key_name: the name of the key
    :param partial_string: substring of the goal string (first name of the person for instance, or "Samsung", instead of
        its full legal name).
    :return: a like condition for string in the form of XXX Like '%aa%' or 'TRUE' if one
        of input is empty
    """
    if partial_string == "" or key_name == "":
        return "TRUE"
    return f"{key_name} like \'%{partial_string}%\'"


def generate_year_equal_condition(key_name: str, exact_year: str) -> str:
    """
    return an equal condition for year
    :param key_name: the name of the key
    :type key_name: str
    :param exact_year: a string represent the exact year we are looking for
    :type exact_year: str
    :return: an equal condition for time in the form of strftime('%Y',key_name) = 'exact_time}' or 'TRUE' if one
        of input is empty
    :rtype: str
    """
    if key_name == "" or exact_year == "":
        return "TRUE"
    return f"strftime(\'%Y\', {key_name}) = \'{exact_year}\'"


def generate_select_query(selected_key: List[str], the_table_name: str, where_conditions: List[str] = [],
                          group_by: str = '',
                          order_by: str = '') -> str:
    """
    Vanilla, naive method of constructing a select query string
    :param group_by: group by condition
    :type group_by: str
    :param order_by: order by condition
    :type order_by: str
    :param the_table_name: the name of the table which contains the keys we are looking for
    :type the_table_name: string
    :param selected_key: name of keys that will be returned by the query
    :type selected_key: List of string
    :param where_conditions: list of where conditions
    :type where_conditions: List of string
    :return: a string represent the SQLite select query
    :rtype: string
    """
    select_string = 'Select ' + selected_key[0] if len(selected_key) != 0 else 'Select *'
    for variable_name in selected_key[1:]:
        select_string = select_string + ", " + variable_name
    from_string = " From " + the_table_name
    where_string = " Where " + aggregating_conditions(where_conditions) if len(where_conditions) != 0 else ""
    group_by_string = " GROUP BY " + group_by if group_by != '' else ''
    order_by_string = " ORDER BY " + order_by if order_by != '' else ''
    return select_string + from_string + where_string + group_by_string + order_by_string


def get_earliest_year() -> int:
    """
    TODO: Don't hardcode this
    :return: The first year for which a transaction exists in the database
    """
    return 2013


def get_latest_year() -> int:
    """
    TODO: Don't hardcode this
    :return: The last year for which a transaction exists in the database
    """
    return 2022


def get_transactions_between(date_lower: date, date_upper: date) -> list[Transaction]:
    """
    This method makes a database query for all transactions that fall in the inclusive range from date_lower
    to date_upper. The transactions will be represented using the Transaction Dataclass.

    :param date_lower: The lower range of the transaction query
    :param date_upper: The upper range of the transaction query
    :return: A list of all transactions from the database within the given range
    """
    if date_lower < date(get_earliest_year(), 1, 1) or date_upper > date(get_latest_year(), 12, 31):
        return []

    connection = get_db_connection()
    cur = connection.cursor()

    full_query = f"SELECT * FROM {table_name} WHERE transaction_date BETWEEN " \
                 f"'{date_lower.isoformat()}' AND '{date_upper.isoformat()}'"
    cur.execute(full_query)

    connection.commit()
    db_transactions = cur.fetchall()
    print(full_query)
    return convert_db_transactions_to_dataclass(db_transactions)


def convert_db_transactions_to_dataclass(db_transactions: list[sqlite3.Row]) -> list[Transaction]:
    """
    This method takes a list of transactions from the database (matching the sql schema)
    and converts it to a list of Transaction dataclass objects.

    :param db_transactions: The list of transactions returned from a database query
    :return: The given list of transactions represented as Transaction objects
    """
    transactions = []
    for t in db_transactions:
        transaction_type = TransactionType("Purchase" if t["transaction_type"] == "P" else "Sale")
        description = None if t["description"] == "None" else t["description"]
        transactions.append(
            Transaction(t["id"], t["member_name"], District.from_district_string(t["state_district_number"]),
                        t["company"], t["ticker"], transaction_type, date.fromisoformat(t["transaction_date"]),
                        (t["value_lb"], t["value_ub"]), description))

    return transactions


def get_transactions_btwn_years(method: str, request: Request, date_lower: date, date_upper: date) -> list:
    """
    This method makes a database query to list all transactions, with information including the U.S. House
    of Representatives name, U.S. House of Representative district, company, ticker, transaction
    type (purchase or sale), date, the lower and upper bound of the stock purchased/sold,
    description, and link to the official document showing the transaction.

    :param method: string represeting method calling this function (ex. "POST", "GET"...)
    :param request: Flask Request containing the HTML Form Results from transactions_table.html
    :param date_lower: The lower range of the transaction query
    :param date_upper: The upper range of the transaction query
    :return: A list of all transactions from the database within the given date range
    """

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    keys = []
    where_conditions = [value_between("transaction_date", date_lower.isoformat(), date_upper.isoformat(),
                                      bound_is_str=True)]

    if method == "POST" and check_transactions_advanced_search(request): 
        # returns additional where conditions
        where_conditions += get_transactions_advanced_search(request)

    full_query = generate_select_query(keys, table_name, where_conditions)
    cur.execute(full_query)

    connection.commit()
    data = cur.fetchall()

    return data


def get_transactions_advanced_search(request: Request) -> list:
    """
    This method creates the string for a database query for all transactions
    that match the details in the given request.

    :param request: Flask Request containing the HTML Form Results from transaction_table.html
    :return: A list of all transactions from the database matching the given search parameters.
    """

    query_member_name = equal_condition('member_name', request.form['member_name'])
    query_member_district = equal_condition("state_district_number", request.form['distrNum'])
    query_company = equal_condition('company', request.form['company'])
    query_ticker = equal_condition("ticker", request.form['ticker'])
    query_lb = value_greater_equal('value_lb', request.form['lowerBound'])
    query_ub = value_less_equal('value_ub', request.form['upperBound'])
    query_trans_type = equal_condition('transaction_type', request.form['transType'])

    return [query_member_name, query_member_district, query_company, query_ticker, query_lb, query_ub, query_trans_type]


def check_transactions_advanced_search(request: Request) -> bool:
    """
    This method checks whether or not an advanced search was requested

    :param request: Flask Request containing the HTML Form Results from transactions_table.html
    :return: True if an advanced search was requested or False if an advanced search was not requested.
    """

    if request.form['member_name'] != "" or request.form['distrNum'] != "" or request.form['company'] != "" \
            or request.form['ticker'] != "" or request.form['lowerBound'] != "" or request.form['upperBound'] != "" \
            or request.form["transType"] != "":
        return True

    return False


def get_companies_btwn_years(method: str, request: Request, date_lower: date, date_upper: date) -> list:
    """
    This method makes a database query to list all companies with their corresponding ticker,
    the number of transactions including this company, the number of house members that made a transaction
    with this company, and the lower and upper bounds of stock purchases/sales.
    The query will return data that is between the date_lower and date_upper.

    :param method: string represeting method calling this function (ex. "POST", "GET"...)
    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :param date_lower: The lower range of the transaction query
    :param date_upper: The upper range of the transaction query
    :return: A list of all companies along with aggregated columns from the database within the given
    date range
    """

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    temp_query = f"WITH temp AS (SELECT company, ticker, id, member_name, " \
                 f"CASE transaction_type WHEN 'P' THEN value_lb ELSE 0 END AS purchase_lb, " \
                 f"CASE transaction_type WHEN 'P' THEN value_ub ELSE 0 END AS purchase_ub, " \
                 f"CASE transaction_type WHEN 'S' THEN value_lb ELSE 0 END AS sale_lb, " \
                 f"CASE transaction_type WHEN 'S' THEN value_ub ELSE 0 END AS sale_ub " \
                 f"FROM {table_name} " \
                 f"WHERE transaction_date BETWEEN '{date_lower.isoformat()}' AND '{date_upper.isoformat()}')"

    transaction_value = [('P', 'purchase'), ('S', 'sale')]
    boudnary = ['lb', 'ub']

    # temp_table_keys = ["company", "ticker", "id", "member_name"]
    # for val, full_str in transaction_value:
    #     for b in boudnary:
    #         temp_table_keys += [
    #             cases_str(expression="transaction_type", case_value_pairs={val: f'value_{b}'}, else_value=0,
    #                       as_var_name=f'{full_str}_lb', key_is_str=True)]
    
    full_query = f" {temp_query} " \
                 f"SELECT company, ticker, " \
                 f"COUNT(id) AS num_transactions, " \
                 f"COUNT(DISTINCT member_name) AS num_members, " \
                 f"SUM(purchase_lb) as purchase_lb, " \
                 f"SUM(purchase_ub) as purchase_ub, " \
                 f"SUM(sale_lb) as sale_lb, " \
                 f"SUM(sale_ub) as sale_ub " \
                 f"FROM temp "

    if method == "POST" and check_companies_advanced_search(request): 
        # Adds the where clause to the sql query
        full_query += get_companies_advanced_search(request)
    else:
        full_query += " GROUP BY company"

    cur.execute(full_query)
    connection.commit()
    data = cur.fetchall()

    return data


def get_companies_advanced_search(request: Request) -> list:
    """
    This method creates the string for a database query for all companies
    that match the details in the given request.

    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :return: A list of all companies from the database matching the given search parameters
    """

    query_company, query_ticker, query_transaction_count, query_member_count, query_purchaselb, query_purchaseub, \
        query_salelb, query_saleub = get_companies_advanced_search_helper(request)

    where_conditions = [query_company, query_ticker, query_purchaselb, query_purchaseub, query_salelb, query_saleub]
    having_conditions = [query_transaction_count, query_member_count]

    where_string = " WHERE " + aggregating_conditions(where_conditions) if len(where_conditions) != 0 else ""
    having_string = " HAVING " + aggregating_conditions(having_conditions) if len(having_conditions) != 0 else ""

    return where_string + " GROUP BY company" + having_string


def get_companies_advanced_search_helper(request: Request) -> tuple:
    """
    This is a helper method for get_companies_advanced_search() that gets values from the HTML form
    in companies_table.html. This helper function also breaks down the queries into strings
    for get_companies_advanced_search() method.

    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :return: A tuple of strings used for querying the database.
    """

    query_company = equal_condition('company', request.form['company'])
    query_ticker = equal_condition("ticker", request.form['ticker'])
    query_transaction_count = equal_condition('num_transactions', request.form['transCount'], False)
    query_member_count = equal_condition('num_members', request.form['memberCount'], False)
    query_purchaselb = value_greater_equal('purchase_lb', request.form['purchaselb'])
    query_purchaseub = value_less_equal('purchase_ub', request.form['purchaseub'])
    query_salelb = value_greater_equal('sale_lb', request.form['salelb'])
    query_saleub = value_less_equal('sale_ub', request.form['saleub'])

    return query_company, query_ticker, query_transaction_count, query_member_count, query_purchaselb, \
        query_purchaseub, query_salelb, query_saleub


def check_companies_advanced_search(request: Request) -> bool:
    """
    This method checks whether or not an advanced search was requested

    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :return: True if an advanced search was requested or False if an advanced search was not requested.
    """

    if request.form['company'] != "" or request.form['ticker'] != "" or request.form['transCount'] != "" \
            or request.form['memberCount'] != "" or request.form['purchaselb'] != "" \
            or request.form['purchaseub'] != "" or request.form['salelb'] != "" or request.form['saleub'] != "":
        return True

    return False
