import sqlite3
from flask import Request
from datetime import date

from cstm.enums import TransactionType
from cstm.dataclasses import Transaction, District

db_file_path = r"database/database.db"
table_name = r"all_transaction"


def get_db_connection(db_file: str = db_file_path):
    """
    :param db_file: Database file path
    :return: SQL3 Database Connection for the given file
    """
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


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


def transaction_query(request: Request) -> list:
    """
    This method makes a database query for all transactions that match the details in the given request. This request
    is expected to be generated from an HTML form, and could contain all the fields present in the form found in
    index.html's form

    :param request: Flask Request containing the HTML Form Results from index.html
    :return: A list of all transactions in the database matching the given search parameters
    """

    member_name = request.form['member_name']
    transaction_year = request.form['transaction_year']
    company = request.form['company']

    query_member_name = f"member_name = \'{member_name}\'" if member_name != "" else 'TRUE'
    # need to check what kind of value is returned by the transaction_date query_transaction_date = f"AND
    # transaction_date = \'{transaction_date}\'" if transaction_date != "" else 'TRUE'
    query_company = f"AND company = \'{company}\'" if company != "" else 'AND TRUE'
    query_transaction_year = f"AND strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" \
        if transaction_year != "" else 'AND TRUE'

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    full_query = f'select *  from {table_name} where {query_member_name} {query_transaction_year} {query_company}'
    print(full_query)
    cur.execute(full_query)

    connection.commit()
    data = cur.fetchall()
    if len(data) == 0 and member_name == 'all':
        cur.execute(f"select * from {table_name}")
        connection.commit()
        data = cur.fetchall()

    return data


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


def get_most_popular_companies(request: Request) -> list:
    """
    This method makes a database query for all companies with the greatest amount of transactions depending on
    that match the details in the given request. This request is expected to be generated from an HTML form found
    at companies_table.html

    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :return: A list of all companies from the database matching the given search parameters, sorted by the greatest
    number of transactions.
    """

    query_company, query_ticker, query_trans_type, query_transaction_year, select_query_year = \
        get_most_popular_companies_helper(request)

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    full_query = f'SELECT ROW_NUMBER() OVER(ORDER BY COUNT(id) DESC) AS rank, company, ticker, transaction_type, ' \
                 f'IFNULL({select_query_year}, \'All\') AS year, COUNT(id) AS num_transactions, ' \
                 f'COUNT(DISTINCT member_name) AS num_members, SUM(value_lb) AS value_lb, SUM(value_ub) AS value_ub ' \
                 f'FROM {table_name} WHERE {query_transaction_year} {query_company} {query_ticker} ' \
                 f'{query_trans_type} GROUP BY company ORDER BY num_transactions DESC'

    cur.execute(full_query)

    connection.commit()
    data = cur.fetchall()

    return data


def get_most_popular_companies_helper(request: Request) -> tuple:
    """
    This is a helper method for most_popular_companies() that gets values from the HTML form
    in companies_table.html. This helper function also breaks down the queries to be more readable
    for most_popular_companies() method.

    :param request: Flask Request containing the HTML Form Results from companies_table.html
    :return: A tuple of strings used for querying the database.
    """

    transaction_year = request.form['transaction_year']
    company = request.form['company']
    ticker = request.form['ticker']
    transaction_type = request.form['transaction_type']

    query_transaction_year = f"strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" if transaction_year != "" \
        else 'TRUE'
    query_company = f"AND company = \'{company}\'" if company != "" else 'AND TRUE'
    query_ticker = f"AND ticker = \'{ticker}\'" if ticker != "" else 'AND TRUE'
    query_trans_type = f"AND transaction_type = \'{transaction_type}\'" \
        if transaction_type == "S" or transaction_type == "P" else 'AND TRUE'

    select_query_year = f"strftime(\'%Y\',transaction_date)" if transaction_year != "" else f"NULL"

    return query_company, query_ticker, query_trans_type, query_transaction_year, select_query_year
