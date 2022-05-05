from visualization.helper_functions import purchase_sale_sum_on_time, row_lst_to_pandas_dataframe, \
    purchase_sale_vs_time_visual_graph_json
from flask import Request
from datetime import date, datetime, timedelta
from cstm.database_helpers import get_db_connection

database_path = r"database/database.db"


def purchase_sale_vs_time(request: Request) -> str:
    """
    return the purchase/sale value vs time graph json str
    :param request: Request object from flask
    :type request: flask.Request
    :return: json str (encoded graph)
    :rtype: str
    """

    # TODO: check with Brian what is the format of time string returned in flask.Request
    # TODO: see if we keep 60 days default range
    date_lower: date = datetime.now() - timedelta(days=60)
    date_upper: date = datetime.now()

    ticker = request.form.get('ticker')
    company_name = request.form.get('company_name')
    member_name = request.form.get('member_name')

    full_query = purchase_sale_sum_on_time(date_lower, date_upper, ticker, company_name, member_name)

    conn = get_db_connection(database_path)
    cur = conn.cursor()

    data = cur.execute(full_query)
    column_names = [col[0] for col in data.description]
    data = data.fetchall()
    data_frame = row_lst_to_pandas_dataframe(data, column_names)

    return purchase_sale_vs_time_visual_graph_json(data_frame=data_frame)
