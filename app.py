from flask import Flask, render_template, request, url_for, flash, redirect
from typing import List
import sqlite3

app = Flask(__name__)

db_file_path = r"demo.db"
table_name = r"demo_table"

def get_db_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root_dir():
    return render_template('index.html')

@app.route('/list')
def list():
    connection = get_db_connection(db_file_path)
    cur = connection.cursor()
    cur.execute(f"select * from {table_name}")
    entries = cur.fetchall()
    return render_template("all_transaction.html",entries = entries)

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)

