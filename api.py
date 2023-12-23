from flask import Flask, make_response, jsonify, request
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

@app.route('/banks', methods=["GET"])
def get_banks():
    cur = mysql.connection.cursor()
    query="""
    select * from banks
    """
    cur.execute(query)
    data =cur.fetchall()
    cur.close()
    
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)