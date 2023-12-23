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

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def index():
    return 'Index Page'

@app.route('/banks', methods=["GET"])
def get_banks():
    query="""
    select * from banks
    """
    
    data = data_fetch(query)
    
    return make_response(jsonify(data), 200)

@app.route("/banks/<int:id>", methods=["GET"])
def GetBankById(id):
    query="""
    SELECT * FROM banks WHERE banks_id = {}
    """.format(id)
    
    data = data_fetch(query)
    
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)