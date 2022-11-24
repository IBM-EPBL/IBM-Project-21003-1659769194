#!/usr/bin/env python

from flask import Flask,render_template,request,redirect,url_for,session
from datetime import date
import ibm_db
import bcrypt
import re
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app=Flask(__name__)
app.secret_key='a'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dgp98488;PWD=T4ZhPsFfVgztgO7H;","","")

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/display')
def display():
    print (session["email"],session["id"])

@app.route("/api/login",methods=['POST'])
def login():
    msg={};
    if request.method=="POST":
        email=request.form['email']
        password=request.form['pw']
        sql="SELECT * from test where email=?;"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        if account and bcrypt.checkpw(password.encode('utf-8'), account["PASSWORD"].encode('utf-8')):
            session['Loggedin']=True
            session['id']=account['USERID']
            session['email']=account['EMAIL']
            session['name']=account['USERNAME']
            msg={"Success": True}
        else:
            msg={"Success": False, "msg": "Account does not exist! Please Register!"}
    return json.dumps(msg)

@app.route("/api/register",methods=["POST"])
def register():
    msg={}
    if request.method=="POST":
        username=request.form['name']
        email=request.form['email']
        password=request.form['pass']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql="SELECT * FROM test where username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        if account:
            msg={"Success": False, "msg": "Account already exists!!"}
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg={"Success": False, "msg": "Invalid Email Address!"}
        elif not re.match(r'([a-zA-Z]|[0-9])+',username):
            msg={"Success": False, "msg": "Name must contain only characters and numbers!"}
        else:
            insert_sql="INSERT into test(email, username, password) values (?,?,?);"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,email)
            ibm_db.bind_param(prep_stmt,2,username)
            ibm_db.bind_param(prep_stmt,3,hashed)
            ibm_db.execute(prep_stmt)
            msg={"Success": True, "msg": "You have registered for the App successfully!"}
    return json.dumps(msg)

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    if "id" in session.keys():
        user = session["id"]
        date_now = request.form["date"]
        amount = request.form["amount"]
        category = request.form["category"]
        insert_sql="INSERT into expenses(user, date, amount, category) values (?,?,?,?);"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,user)
        ibm_db.bind_param(prep_stmt,2,date_now)
        ibm_db.bind_param(prep_stmt,3,amount)
        ibm_db.bind_param(prep_stmt,4,category)
        msg = {"msg": f"{ibm_db.execute(prep_stmt)}",}
        send(user, session["email"])
        return json.dumps(msg);
    return json.dumps({"msg": "Invalid session: Log in"});

@app.route("/api/expenses", methods=["GET"])
def view_expense():
    if "id" in session.keys():
        user = session["id"]
        sql_stmt="SELECT * from expenses where expenses.user=?"
        stmt=ibm_db.prepare(conn,sql_stmt)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_assoc(stmt)
        ret = []
        while row != False:
            ret.append({"user":row["USER"], "amount": -row["AMOUNT"], "category": row["CATEGORY"], "date": f"{row['DATE']}"})
            row = ibm_db.fetch_assoc(stmt)
        return json.dumps(ret)
    return json.dumps({"msg": "Invalid session: Log in"});

@app.route("/api/expenses_by_category", methods=["GET"])
def view_expense_by_catergory():
    if "id" in session.keys():
        user = session["id"]
        sql_stmt="SELECT category, SUM(amount) as amount from expenses where expenses.user=? and amount>0 group by category"
        stmt=ibm_db.prepare(conn,sql_stmt)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_assoc(stmt)
        ret = {"food":0,"entertainment":0,"shopping":0, "emi": 0, "rent":0, "others": 0}
        while row != False:
            ret[row["CATEGORY"]]= row["AMOUNT"]
            row = ibm_db.fetch_assoc(stmt)
        return json.dumps(ret)
    return json.dumps({"msg": "Invalid session: Log in"});

@app.route("/api/balance", methods=["GET"])
def view_balance():
    if "id" in session.keys():
        user = session["id"]
        sql_stmt="SELECT SUM(amount) as balance from expenses where expenses.user=?"
        stmt=ibm_db.prepare(conn,sql_stmt)
        ibm_db.bind_param(stmt,1,user)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_assoc(stmt)
        ret = {};
        if row != False and row["BALANCE"]!=None:
            ret["balance"]= -row["BALANCE"];
        else:
            ret["balance"]= 0;
        return json.dumps(ret)
    return json.dumps({"msg": "Invalid session: Log in"});

@app.route("/api/session", methods=["GET"])
def get_session():
    if "id" in session.keys():
        ret = {}
        ret['id']=session['id']
        ret['email']=session['email']
        ret['name']=session['name']
        return json.dumps(ret)
    return json.dumps({"msg": "Invalid session: Log in"});

@app.route("/api/session", methods=["DELETE"])
def clear_session():
    session.clear();
    return json.dumps({"Success":True})

def send(user, email):
    sql_stmt="SELECT SUM(amount) as balance from expenses where expenses.user=?"
    stmt=ibm_db.prepare(conn,sql_stmt)
    ibm_db.bind_param(stmt,1,user)
    ibm_db.execute(stmt)
    row = ibm_db.fetch_assoc(stmt)
    ret = {};
    if row != False and row["BALANCE"]!=None and row["BALANCE"]>0:
        message=Mail(from_email='ramyanmsr@gmail.com',
                     to_emails=email,
                     subject='ALERT!! Budget Exceeded!',
                     plain_text_content='Budget has been crossed for this month',
                     html_content='<strong>Hi user,<br> You have crossed your budget for this month. ---you  have made max expenditure in so and so category! Its a remainder for you to start saving!  </strong>')
        try:
            """sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))"""
            sg = SendGridAPIClient('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')
            response=sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    app.run(debug=True)
