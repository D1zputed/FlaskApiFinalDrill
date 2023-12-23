from flask import Flask
from flask_mysqldb import MySQL
from markupsafe import escape

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "loan_management"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'