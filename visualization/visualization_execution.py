from visualization.helper_functions import purchase_sale_sum_on_time, row_lst_to_pandas_dataframe, \
    purchase_sale_vs_time_visual_graph
import json
from flask import Request
from plotly.utils import PlotlyJSONEncoder
from datetime import date, datetime
from cstm.database_helpers import get_db_connection

database_path = r"database/database.db"


def purchase_sale_vs_time(request: Request) -> str:  # pragma: no cover
    """
    return the purchase/sale value vs time graph json str
    :param request: Request object from flask
    :type request: flask.Request
    :return: json str (encoded graph)
    :rtype: str
    """

    # TODO: check with Brian what is the format of time string returned in flask.Request
    # TODO: see if we keep 60 days default range
    date_lower: date = datetime(2013,1,1)
    date_upper: date = datetime.now()

    ticker = str(request.form.get('ticker') or "")
    company = str(request.form.get('company') or "")
    member_name = str(request.form.get('member_name') or "")

    full_query = purchase_sale_sum_on_time(date_lower, date_upper, ticker, company, member_name)

    conn = get_db_connection(database_path)
    cur = conn.cursor()

    data = cur.execute(full_query)
    column_names = ['transaction_date', 'purchase_lb', 'purchase_ub', 'sale_lb', 'sale_ub']
    data = data.fetchall()
    data_frame = row_lst_to_pandas_dataframe(data, column_names)

    return json.dumps(purchase_sale_vs_time_visual_graph(data_frame=data_frame), cls=PlotlyJSONEncoder)
