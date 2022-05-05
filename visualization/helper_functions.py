import sqlite3
import json
import pandas

from datetime import date, datetime

from plotly import express as px, graph_objs as go
from plotly.utils import PlotlyJSONEncoder

from cstm.database_helpers import generate_select_query, generate_string_like_condition, generate_year_equal_condition, \
    table_name, get_db_connection
from cstm.query import value_between, value_greater_equal, value_less_equal, equal_condition, aggregating_conditions, \
    expression_wrapper, where_condition


def purchase_sale_conversion_query():
    """
    return the query that convert value_lb and value_ub based on transaction type
    i.e., change it into purchase_lb/purchase_ub when transaction_type is 'P',
    sale_lb/sale_ub otherwise
    :return: a string that represent the sql query
    """

    keys = ['company', 'ticker', 'id', 'member_name', 'transaction_date',
            "CASE transaction_type WHEN 'P' THEN value_lb ELSE 0 END AS purchase_lb",
            "CASE transaction_type WHEN 'P' THEN value_ub ELSE 0 END AS purchase_ub",
            "CASE transaction_type WHEN 'S' THEN value_lb ELSE 0 END AS sale_lb",
            "CASE transaction_type WHEN 'S' THEN value_ub ELSE 0 END AS sale_ub"]
    return generate_select_query(selected_key=keys, the_table_name=table_name)


def purchase_sale_sum_on_time(date_lower: date, date_upper: date, ticker: str, company_name: str, member_name: str):
    """
    helper function that generate the query which sum purchase/sale value that occurs on same day
    :param member_name: name of congress member
    :type member_name: str
    :param ticker: name of ticker
    :type ticker: str
    :param company_name: name of company
    :type company_name: str
    :param date_lower: date range lower bound (transaction_date >= date_lower)
    :type date_lower: date
    :param date_upper: date range upper bound (transaction_date <= date_lower)
    :type date_upper: date
    :return: the sql query
    :rtype: str
    """
    temp_query = purchase_sale_conversion_query()
    keys = ["COUNT(id) AS num_transactions",
            "COUNT(DISTINCT member_name) AS num_members",
            "SUM(purchase_lb) as purchase_lb",
            "SUM(purchase_ub) as purchase_ub",
            "SUM(sale_lb) as sale_lb",
            "SUM(sale_ub) as sale_ub",
            "strftime(\'%d-%m-%Y\', transaction_date) as transaction_date "]

    time_range = value_between(expression='transaction_date', lower_bound=date_lower.strftime('%d-%m-%Y'),
                               upper_bound=date_upper.strftime('%d-%m-%Y'), bound_is_str=True)

    ticker_equal = equal_condition(expression='ticker', exact_value=ticker, value_is_string=True)
    company_name_equal = equal_condition(expression='company_name', exact_value=company_name, value_is_string=True)
    member_name_equal = equal_condition(expression='member_name', exact_value=member_name, value_is_string=True)

    full_query = f'WITH temp as ({temp_query})' + generate_select_query(selected_key=keys, the_table_name='temp',
                                                                        where_conditions=[time_range, ticker_equal,
                                                                                          member_name_equal,
                                                                                          company_name_equal],
                                                                        group_by='transaction_date')
    return full_query


def convert_date_string_lst_to_datetime(string_lst: list[str], str_format: str) -> list[datetime]:
    return [datetime.strptime(date_str, str_format) for date_str in string_lst]


def row_lst_to_pandas_dataframe(data: list[sqlite3.Row], column_names: list[str]) -> pandas.DataFrame:
    """
    convert the input list of Row objects into pandas dataframe with given column names
    :param column_names: list of column names
    :type column_names: list[str]
    :param data: list of sqlite3 rows
    :type data: sqlite3.Row
    :return: a pandas dataframe
    :rtype: pandas.DataFrame
    """
    result: list[list] = []
    for column in column_names:
        result.append([row[column] for row in data])

    result: pandas.DataFrame = pandas.DataFrame(result).transpose()
    result.columns = column_names
    return result


def purchase_sale_vs_time_visual_graph_json(data_frame: pandas.DataFrame) -> str:
    """
    using data in dataframe, construct a purchase/sale value vs time graph using plotly and encode the graph into jason
    then return the json string.
    :param data_frame: the data (should contain purchase_lb, purchase_ub, sale_lb, sale_ub, transaction_date)
    :type data_frame: pandas.DataFrame
    :return: a json string
    :rtype: str
    """
    barmode = 'overlay'
    fig = px.histogram(data_frame=data_frame, x='transaction_date', y=data_frame.columns, barmode=barmode)
    return json.dumps(fig, cls=PlotlyJSONEncoder)
