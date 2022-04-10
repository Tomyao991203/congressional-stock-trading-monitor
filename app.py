from flask import Flask, render_template, request, url_for, flash, redirect
from typing import List
import sqlite3

app = Flask(__name__)

db_file_path = r"database/v1.db"
table_name = r"all_transaction"

def get_db_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/',  methods=['GET', 'POST'])
def root_dir():
    if request.method == "POST":
        member_name = request.form['member_name'] 
        transaction_date = request.form['transaction_date'] 
        transaction_year = request.form['transaction_year']
        company = request.form['company'] 
        #may not properly handle empty name. go look at warning later
        
        query_member_name = f"member_name = \'{member_name}\'" if member_name != "" else 'TRUE'
        query_transaction_date = f"AND transaction_date = \'{transaction_date}\'" if transaction_date != "" else 'TRUE'
        query_company = f"AND company = \'{company}\'" if company != "" else 'TRUE'
        query_transaction_year = f"AND EXTRACT(YEAR from transaction_date) = \'{transaction_year}\'" if transaction_year != "" else 'TRUE'
        
        connection = get_db_connection(db_file_path)
        cur = connection.cursor()
        
        full_query = f'select * from {table_name} where {query_member_name} {query_transaction_date} {query_transaction_year} {query_company}'
        print (full_query)
        cur.execute(full_query)
        
        connection.commit()
        data = cur.fetchall()
        
        if len(data) == 0 or member_name == 'all': 
            cur.execute(f"select * from {table_name}")
            connection.commit()
            data = cursor.fetchall()
        return render_template('index.html', data=data)
    return render_template("index.html")

@app.route('/list')
def list():
    connection = get_db_connection(db_file_path)
    cur = connection.cursor()
    cur.execute(f"select * from {table_name}")
    entries = cur.fetchall()
    return render_template("all_transaction.html",entries = entries)

@app.route('/search_by_name', methods=['GET', 'POST'])
def get_transaction_base_on_name():
    if request.method == "POST":
        member_name = request.form['member_name'] 
        transaction_date = request.form['transaction_date'] 
        transaction_year = request.form['transaction_year']
        company = request.form['company'] 
        
        query_member_name = f"member_name = \'{member_name}\'" if member_name != "" else 'TRUE'
        # need to check what kind of value is returned by the transaction_date
        # query_transaction_date = f"AND transaction_date = \'{transaction_date}\'" if transaction_date != "" else 'TRUE'
        query_company = f"AND company = \'{company}\'" if company != "" else 'AND TRUE'
        query_transaction_year = f"AND strftime(\'%Y\',transaction_date) = \'{transaction_year}\'" if transaction_year != "" else 'AND TRUE'
        
        connection = get_db_connection(db_file_path)
        cur = connection.cursor()
        
        full_query = f'select *  from {table_name} where {query_member_name} {query_transaction_year} {query_company}'
        print (full_query)
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