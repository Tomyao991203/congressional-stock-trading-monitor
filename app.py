from flask import Flask, render_template, request
from cstm.query import where_condition
import sqlite3

application = app = Flask(__name__)

db_file_path = r"database/v1.db"
table_name = r"all_transaction"


def get_db_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
def root_dir():
    if request.method == "POST":
        member_name = request.form['member_name']
        # transaction_date = request.form['transaction_date']
        transaction_year = request.form['transaction_year']

        company = request.form['company']

        condition_member_name = where_condition('member_name', member_name)
        condition_company = where_condition('company', company)

        query_transaction_year = f"strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" \
            if transaction_year != ""else 'AND TRUE'

        connection = get_db_connection(db_file_path)
        cur = connection.cursor()

        full_query = f'select *  from {table_name} where {condition_member_name} AND {condition_company} \
            AND {query_transaction_year}'

        cur.execute(full_query)

        connection.commit()
        data = cur.fetchall()

        if len(data) == 0 and member_name == 'all':
            cur.execute(f"select * from {table_name}")
            connection.commit()
            data = cur.fetchall()
        return render_template('index.html', data=data)
    return render_template("index.html")


@app.route('/list')
def list():
    connection = get_db_connection(db_file_path)
    cur = connection.cursor()
    cur.execute(f"select * from {table_name}")
    entries = cur.fetchall()
    return render_template("all_transaction.html", entries=entries)


@app.route('/search_by_name', methods=['GET', 'POST'])
def get_transaction_base_on_name():
    if request.method == "POST":
        member_name = request.form['member_name']
        transaction_year = request.form['transaction_year']
        company = request.form['company']

        condition_member_name = where_condition('member_name', member_name)
        condition_company = where_condition('company', company)

        query_transaction_year = f"strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" \
            if transaction_year != "" else 'AND TRUE'

        connection = get_db_connection(db_file_path)
        cur = connection.cursor()

        full_query = f'select *  from {table_name} where {condition_member_name} AND {condition_company} \
            AND {query_transaction_year}'

        cur.execute(full_query)

        connection.commit()
        data = cur.fetchall()
        if len(data) == 0 and member_name == 'all':
            cur.execute(f"select * from {table_name}")
            connection.commit()
            data = cur.fetchall()
        return render_template('search_by_name.html', data=data)
    return render_template("search_by_name.html")


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
