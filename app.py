from flask import Flask, render_template, request, redirect
from datetime import date

from cstm.database_helpers import get_most_popular_companies, transaction_query, get_latest_year, get_earliest_year
from cstm.representative_helpers import representative_list

application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root_dir():
    if request.method == "POST":
        return render_template("transactions.html", data=transaction_query(request), dark_mode=is_dark_mode())
    return render_template("transactions.html", dark_mode=is_dark_mode())


@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if request.method == 'POST':
        return render_template("companies.html", data=get_most_popular_companies(request), dark_mode=is_dark_mode())
    return render_template("companies.html", dark_mode=is_dark_mode())


@app.route('/representatives', methods=['GET', 'POST'])
def representatives():
    today = date.today()
    year_start = date(today.year, 1, 1)
    if request.method == 'POST':
        range_start = date.fromisoformat(request.form["range_start"])
        range_end = date.fromisoformat(request.form["range_end"])
        rep_list = representative_list(range_start, range_end)
    else:
        rep_list = representative_list(year_start, today)
    return render_template("representatives.html", representatives=rep_list, start=get_earliest_year(),
                           today=today, year_start=year_start, dark_mode=is_dark_mode())


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
