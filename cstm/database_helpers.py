import sqlite3
from flask import Request
from typing import List

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


def generate_like_condition_string(variable_name: str, partial_value: str) -> str:
    """
    return a like condition (SQLite)
    :param variable_name: the name of the variable
    :param partial_value: substring of the goal string (first name of the person for instance, or "Samsung", instead of
        its full legal name).
    :return: a like condition string in the form of XXX Like %aa%
    """
    if partial_value is "" or variable_name is "":
        return "TRUE"
    return f"{variable_name} like \'%{partial_value}%\'"


def generate_equal_condition_string(variable_name: str, partial_value: str) -> str:
    """
    return an equal condition (SQLite)
    :param variable_name: the name of the variable
    :param partial_value: the goal string
    :return:
    """
    if partial_value is "" or variable_name is "":
        return "TRUE"
    return f"{variable_name} = \"{partial_value}\""


def generate_select_query(selected_var: List[str], the_table_name: str, where_conditions: List[str]) -> str:
    """
    Vanilla, naive method of constructing a select query string
    :param the_table_name: the name of the table which contains the keys we are looking for
    :type the_table_name: string
    :param selected_var: name of keys that will be returned by the query
    :type selected_var: List of string
    :param where_conditions: list of where conditions
    :type where_conditions: List of string
    :return: a string represent the SQLite select query
    :rtype: string
    """
    select_string = 'Select ' + selected_var[0] if len(selected_var) != 0 else 'Select *'
    for variable_name in selected_var:
        select_string = select_string + ", " + variable_name
    from_string = " From " + the_table_name
    where_string = "Where " + where_conditions[0] if len(where_conditions) != 0 else ""
    for condition in where_conditions:
        where_string = where_string + " And " + condition
    return select_string + from_string + where_string

def transaction_query(request: Request) -> list:
    """
    This method makes a database query for all transactions that match the details in the given request. This request
    is expected to be generated from an HTML form, and could contain all the fields present in the form found in
    index.html's form

    :param request: Flask Request containing the HTML Form Results from index.html
    :return: A list of all transactions in the database matching the given search parameters
    """
    # TODO: make a condition in which if the full equal query return nothing, use the like query

    member_name = request.form['member_name']
    transaction_year = request.form['transaction_year']
    company = request.form['company']

    query_member_name = f"member_name = \'{member_name}\'" if member_name != "" else 'TRUE'
    query_company = f"AND company = \'{company}\'" if company != "" else 'AND TRUE'
    query_transaction_year = f"AND strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" \
        if transaction_year != "" else 'AND TRUE'

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    full_query = f'select * from {table_name} where {query_member_name} {query_transaction_year} {query_company}'
    print(full_query)
    cur.execute(full_query)

    connection.commit()
    data = cur.fetchall()
    if len(data) == 0 and member_name == 'all':
        cur.execute(f"select * from {table_name}")
        connection.commit()
        data = cur.fetchall()

    return data
