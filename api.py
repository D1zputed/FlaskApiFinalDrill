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

@app.route("/banks", methods=["POST"])
def AddBank():
    cur = mysql.connection.cursor()
    info = request.get_json()
    banks_id = info["banks_id"]
    banks_details = info["banks_details"]
    query = f"""INSERT INTO banks VALUES ({banks_id}, "{banks_details}")"""
    cur.execute(query)
    
    mysql.connection.commit()
    cur.close()
    
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "bank added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/banks/<int:id>", methods=["PUT"])
def UpdateBankDetails(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    
    banks_details = info["bank_details"]
    query = f"""UPDATE banks SET bank_details = "{banks_details}" WHERE banks_id = {id}"""
    
    cur.execute(query)
    
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "bank updated successfully", "rows_affected": rows_affected}
        ),20,
    )

@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    cur = mysql.connection.cursor()
    query = f""" DELETE FROM transactions WHERE transaction_id = {id} """
    cur.execute(query)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "transaction deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)