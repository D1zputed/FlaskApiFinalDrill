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

@app.route("/banks/type", methods=["GET"])
def GetType():
    query="""
    SELECT * FROM accounts WHERE account_number IN 
    (SELECT account_number FROM transactions where transaction_type_code = 0)
    """
    
    data = data_fetch(query)
    
    return make_response(jsonify(data), 200)

@app.route("/banks/<int:id>/customers", methods=["GET"])
def GetCustomerBanks(id):
    query="""
    Select customers.personal_details, customers.contact_details, banks.bank_details
    FROM branches inner join customers on customers.branch_id = branches.branch_id
    inner join banks on banks.banks_id = branches.bank_id 
    WHERE banks.banks_id = {}
    """.format(id)
    
    data = data_fetch(query)
    
    return make_response(jsonify(data), 201)

if __name__ == "__main__":
    app.run(debug=True)