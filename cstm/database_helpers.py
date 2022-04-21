import sqlite3
from flask import Request

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
