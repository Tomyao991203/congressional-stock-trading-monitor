from flask import Flask, render_template, request
from cstm.database_helpers import transaction_query
import sqlite3

application = app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root_dir():
    if request.method == "POST":
        return render_template('index.html', data=transaction_query(request))
    return render_template("index.html")


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
