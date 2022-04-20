import sqlite3
from flask import Request
from typing import List

db_file_path = r"C:\Users\tomya\OneDrive\CMSC435\CMSC435_demo\database\database.db"
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


def generate_string_equal_condition(key_name: str, exact_string: str) -> str:
    """
    return an equal condition for string (SQLite)
    :param key_name: the name of the key
    :param exact_string: the goal string
    :return: an equal condition for string in the form of XXX = 'aa' or 'TRUE' if one
        of input is empty
    """
    if exact_string == "" or key_name == "":
        return "TRUE"
    return f"{key_name} = \"{exact_string}\""


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
    return f"strftime(\'%Y\',{key_name}) = \'{exact_year}\'"


def generate_select_query(selected_key: List[str], the_table_name: str, where_conditions: List[str]) -> str:
    """
    Vanilla, naive method of constructing a select query string
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
    where_string = " Where " + where_conditions[0] if len(where_conditions) != 0 else ""
    for condition in where_conditions[1:]:
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

    # query_member_name = f"member_name = \'{member_name}\'" if member_name != "" else 'TRUE'
    # query_company = f"AND company = \'{company}\'" if company != "" else 'AND TRUE'
    # query_transaction_year = f"AND strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" \
    #     if transaction_year != "" else 'AND TRUE'
    full_equal_conditions = [generate_string_equal_condition('member_name', member_name),
                             generate_year_equal_condition('transaction_date', transaction_year),
                             generate_string_equal_condition('company', company)]

    string_like_time_equal_conditions = [generate_string_like_condition('member_name', member_name),
                                         generate_year_equal_condition('transaction_date', transaction_year),
                                         generate_string_like_condition('company', company)]

    selected_keys = []
    equal_query = generate_select_query(selected_keys, table_name, full_equal_conditions)
    like_query = generate_select_query(selected_keys, table_name, string_like_time_equal_conditions)

    connection = get_db_connection(db_file_path)
    cur = connection.cursor()

    cur.execute(equal_query)

    connection.commit()
    data = cur.fetchall()
    if len(data) == 0:
        if member_name == 'all':
            cur.execute(f"select * from {table_name}")
        else:
            cur.execute(like_query)
        connection.commit()
        data = cur.fetchall()

    return data
