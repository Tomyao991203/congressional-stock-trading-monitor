from flask import Flask, render_template, request, redirect
from datetime import date
from json import loads

from cstm.database_helpers import get_transactions_btwn_years, get_companies_btwn_years, get_earliest_year, get_representatives_btwn_years
from cstm.representative_helpers import representative_list
from visualization.visualization_execution import purchase_sale_vs_time

application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root_dir():
    today = date.today()
    year_start = date(today.year, 1, 1)
    cookie = request.cookies.get('categories')
    if cookie:
        categories = list(loads(cookie).keys())
    else:
        categories = []
    if request.method == 'POST':
        range_start = date.fromisoformat(request.form["range_start"])
        range_end = date.fromisoformat(request.form["range_end"])
        transactions_list = get_transactions_btwn_years("POST", request, range_start, range_end)
    else:
        transactions_list = get_transactions_btwn_years("GET", request, year_start, today)
    return render_template("transactions.html", data=transactions_list, start=get_earliest_year(),
                           today=today, year_start=year_start, dark_mode=is_dark_mode(), categories=categories)


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    today = date.today()
    year_start = date(today.year, 1, 1)
    if request.method == 'POST':
        range_start = date.fromisoformat(request.form["range_start"])
        range_end = date.fromisoformat(request.form["range_end"])
        companies_list = get_companies_btwn_years("POST", request, range_start, range_end)
    else:
        companies_list = get_companies_btwn_years("GET", request, year_start, today)
    return render_template("companies.html", companies=companies_list, start=get_earliest_year(),
                           today=today, year_start=year_start, dark_mode=is_dark_mode())


@app.route('/representatives', methods=['GET', 'POST'])
def representatives():
    today = date.today()
    year_start = date(today.year, 1, 1)
    if request.method == 'POST':
        range_start = date.fromisoformat(request.form["range_start"])
        range_end = date.fromisoformat(request.form["range_end"])
        rep_list = get_representatives_btwn_years("POST", request, range_start, range_end)
    else:
        rep_list = get_representatives_btwn_years("GET", request, year_start, today)
    return render_template("representatives.html", representatives=rep_list, start=get_earliest_year(),
                           today=today, year_start=year_start, dark_mode=is_dark_mode())


@app.route('/visualizations', methods=['GET', 'POST'])
def visualizations():
    return render_template("visualizations.html", graphJSON=purchase_sale_vs_time(request),
                            dark_mode=is_dark_mode())


@app.route('/dark_mode')
def set_dark_mode():
    res = redirect("/")
    res.set_cookie('dark_mode', "True")
    return res


@app.route('/light_mode')
def set_light_mode():
    res = redirect("/")
    res.set_cookie("dark_mode", "False")
    return res


def is_dark_mode():
    return "False" if "dark_mode" not in request.cookies else request.cookies["dark_mode"]


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
