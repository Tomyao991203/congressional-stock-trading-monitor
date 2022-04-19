from flask import Flask, render_template, request, make_response, redirect
from cstm.database_helpers import get_most_popular_companies, transaction_query
import sqlite3

application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root_dir():
    dark_mode = "False" if "dark_mode" not in request.cookies else request.cookies["dark_mode"]
    if request.method == "POST":
        return render_template('transactions.html', data=transaction_query(request), dark_mode=dark_mode)
    return render_template("transactions.html", dark_mode=dark_mode)

@app.route('/companies', methods=['GET', 'POST'])
def companies():
    dark_mode = "False" if "dark_mode" not in request.cookies else request.cookies["dark_mode"]
    if request.method == "POST":
        return render_template('companies.html', data=get_most_popular_companies(request), dark_mode=dark_mode)
    return render_template("companies.html", dark_mode=dark_mode)

@app.route('/dark_mode')
def dark_mode():
    res = redirect("/")
    res.set_cookie('dark_mode', "True")
    return res

@app.route('/light_mode')
def light_mode():
    res = redirect("/")
    res.set_cookie("dark_mode", "False")
    return res

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
