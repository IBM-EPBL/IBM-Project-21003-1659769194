# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request, redirect, session 
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
import re

from flask_db2 import DB2
import ibm_db
import ibm_db_dbi
from sendemail import sendgridmail,sendmail

# from gevent.pywsgi import WSGIServer
import os


app = Flask(__name__)

app.secret_key = 'a'
  
# app.config['MYSQL_HOST'] = 'remotemysql.com'
# app.config['MYSQL_USER'] = 'D2DxDUPBii'
# app.config['MYSQL_PASSWORD'] = 'r8XBO4GsMz'
# app.config['MYSQL_DB'] = 'D2DxDUPBii'
"""
dsn_hostname = "ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "vmk08423"
dsn_pwd = "3KfJl6HGDtPdbIWy"
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_port = "31321"
dsn_protocol = "tcpip"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)
"""
# app.config['DB2_DRIVER'] = '{IBM DB2 ODBC DRIVER}'
app.config['database'] = 'bludb'
app.config['hostname'] = 'ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
app.config['port'] = '31321'
app.config['protocol'] = 'tcpip'
app.config['uid'] = 'vmk084230'
app.config['pwd'] = '3KfJl6HGDtPdbIWy'
app.config['security'] = 'SSL'
# try:
mysql = DB2(app)
'''
{
  "connection": {
    "cli": {
      "arguments": [
        [
          "-u",
          "mgc79809",
          "-p",
          "JSAP0x7FXgDIo30t",
          "--ssl",
          "--sslCAFile",
          "1dd14d0c-1b52-4f63-a606-53ecba28771d",
          "--authenticationDatabase",
          "admin",
          "--host",
          "2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:32328"
        ]
      ],
      "bin": "db2",
      "certificate": {
        "certificate_base64": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURIVENDQWdXZ0F3SUJBZ0lVT3dvMC9va09CUEN5RjFWeFJxVGhKRW9ubDBVd0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RTVUpOSUVOc2IzVmtJRVJoZEdGaVlYTmxjekFlRncweU1EQTRNRFF3TWpVMwpNalphRncwek1EQTRNREl3TWpVM01qWmFNQjR4SERBYUJnTlZCQU1NRTBsQ1RTQkRiRzkxWkNCRVlYUmhZbUZ6ClpYTXdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFEb0ZFNGQ0SGdOeXZMUVIwR3gKQTB0amRXQnM4NVBjTDNyRStjN1R3K2diRUdQSUxJU0VZV3o4Y1g1TG1XQk0rY1FnOG9VeSsrQXJ3OEoxaXdRZQpySmlIU2I1clF4WTM0c3BQeGRFVEZkWEhScnJhMGU2VmM4MW42TllJL0ZHSnl1Q3hrTG5GMUtFQW9hbHYwaDM2CnhDT0FvcXRwTlFrTzNpMTRGeU0yRDRiajkxckI4RGk4Vy9XMVpVdVhMNGwzZXVLZUVCeTRuZmhJV3kySVc3aUMKbGpMZ3RlN3hZTDVHbVpKOUdsYWtrSnJ1cnpNREFQLzVUYnRlUUIydElodTBRSVRFZHlESVFYUEZGRDBHYzloZAo3M29JdnpVZUJ3VC9uRHN3OTJNNC82SkdtZWpKN0lpdFBTN3Y2a2dlUVhINDlBaUVJNXpQdUVpVzNOYi9GR0pYCmY2a2JBZ01CQUFHalV6QlJNQjBHQTFVZERnUVdCQlR2RzZ2RU5MRjFVbWZnQ003MmxOcmMzSDI2bURBZkJnTlYKSFNNRUdEQVdnQlR2RzZ2RU5MRjFVbWZnQ003MmxOcmMzSDI2bURBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUEwRwpDU3FHU0liM0RRRUJDd1VBQTRJQkFRQTgvdFVnUTZlaTZYWHZndDJ0dUdrbkpva1Y5UWNkaTNZbFVFWkNDUytjClVQZ3NnMnVBMldxcHlWTm1mRkhjcHZ1Vmp0VHRYTmk2NUM2WlZsRnYxc3p1cU9zdFB5bkJ4blN4cUs0dkc0dTkKVjBWRUgxcE1tZnZBSmxkV3c4UEJTZGJtTk1HdGM4SzlwT0o5OVdBQ1ZFRXVXVGdDeHJKTXFBZnpYUXlidUV0dwp0cW1pV2swTmVXNGk5ZEY4S2dTWUVaQWFodXVBSlRldXB2R2RPV1U0eEV4bm03aEVRbmZPV2ZITThDd08xNWFZClRGQ2s0Q0pDUmR4Mlg5U284V3o1Z3MzcncyRkFDQlJyZ0NYeFFDZnZrZTZUdVNHNkxFRHJHbmpWaXVSQkpZdW4KT1RxWXROaVBHaHpuTHJrL0Fzam1LMzBxQmFLTmFyNUdQajhqalpNb2RiZ04KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
        "name": "1dd14d0c-1b52-4f63-a606-53ecba28771d"
      },
      "composed": [
        "db2 -u mgc79809 -p JSAP0x7FXgDIo30t --ssl --sslCAFile 1dd14d0c-1b52-4f63-a606-53ecba28771d --authenticationDatabase admin --host 2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:32328"
      ],
      "environment": {},
      "type": "cli"
    },
    "db2": {
      "authentication": {
        "method": "direct",
        "password": "JSAP0x7FXgDIo30t",
        "username": "mgc79809"
      },
      "certificate": {
        "certificate_base64": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURIVENDQWdXZ0F3SUJBZ0lVT3dvMC9va09CUEN5RjFWeFJxVGhKRW9ubDBVd0RRWUpLb1pJaHZjTkFRRUwKQlFBd0hqRWNNQm9HQTFVRUF3d1RTVUpOSUVOc2IzVmtJRVJoZEdGaVlYTmxjekFlRncweU1EQTRNRFF3TWpVMwpNalphRncwek1EQTRNREl3TWpVM01qWmFNQjR4SERBYUJnTlZCQU1NRTBsQ1RTQkRiRzkxWkNCRVlYUmhZbUZ6ClpYTXdnZ0VpTUEwR0NTcUdTSWIzRFFFQkFRVUFBNElCRHdBd2dnRUtBb0lCQVFEb0ZFNGQ0SGdOeXZMUVIwR3gKQTB0amRXQnM4NVBjTDNyRStjN1R3K2diRUdQSUxJU0VZV3o4Y1g1TG1XQk0rY1FnOG9VeSsrQXJ3OEoxaXdRZQpySmlIU2I1clF4WTM0c3BQeGRFVEZkWEhScnJhMGU2VmM4MW42TllJL0ZHSnl1Q3hrTG5GMUtFQW9hbHYwaDM2CnhDT0FvcXRwTlFrTzNpMTRGeU0yRDRiajkxckI4RGk4Vy9XMVpVdVhMNGwzZXVLZUVCeTRuZmhJV3kySVc3aUMKbGpMZ3RlN3hZTDVHbVpKOUdsYWtrSnJ1cnpNREFQLzVUYnRlUUIydElodTBRSVRFZHlESVFYUEZGRDBHYzloZAo3M29JdnpVZUJ3VC9uRHN3OTJNNC82SkdtZWpKN0lpdFBTN3Y2a2dlUVhINDlBaUVJNXpQdUVpVzNOYi9GR0pYCmY2a2JBZ01CQUFHalV6QlJNQjBHQTFVZERnUVdCQlR2RzZ2RU5MRjFVbWZnQ003MmxOcmMzSDI2bURBZkJnTlYKSFNNRUdEQVdnQlR2RzZ2RU5MRjFVbWZnQ003MmxOcmMzSDI2bURBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUEwRwpDU3FHU0liM0RRRUJDd1VBQTRJQkFRQTgvdFVnUTZlaTZYWHZndDJ0dUdrbkpva1Y5UWNkaTNZbFVFWkNDUytjClVQZ3NnMnVBMldxcHlWTm1mRkhjcHZ1Vmp0VHRYTmk2NUM2WlZsRnYxc3p1cU9zdFB5bkJ4blN4cUs0dkc0dTkKVjBWRUgxcE1tZnZBSmxkV3c4UEJTZGJtTk1HdGM4SzlwT0o5OVdBQ1ZFRXVXVGdDeHJKTXFBZnpYUXlidUV0dwp0cW1pV2swTmVXNGk5ZEY4S2dTWUVaQWFodXVBSlRldXB2R2RPV1U0eEV4bm03aEVRbmZPV2ZITThDd08xNWFZClRGQ2s0Q0pDUmR4Mlg5U284V3o1Z3MzcncyRkFDQlJyZ0NYeFFDZnZrZTZUdVNHNkxFRHJHbmpWaXVSQkpZdW4KT1RxWXROaVBHaHpuTHJrL0Fzam1LMzBxQmFLTmFyNUdQajhqalpNb2RiZ04KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",
        "name": "1dd14d0c-1b52-4f63-a606-53ecba28771d"
      },
      "composed": [
        "db2://mgc79809:JSAP0x7FXgDIo30t@2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:32328/bludb?authSource=admin&replicaSet=replset"
      ],
      "database": "bludb",
      "host_ros": [
        "2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:30874"
      ],
      "hosts": [
        {
          "hostname": "2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud",
          "port": 32328
        }
      ],
      "jdbc_url": [
        "jdbc:db2://2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud:32328/bludb:user=<userid>;password=<your_password>;sslConnection=true;"
      ],
      "path": "/bludb",
      "query_options": {
        "authSource": "admin",
        "replicaSet": "replset"
      },
      "replica_set": "replset",
      "scheme": "db2",
      "type": "uri"
    }
  },
  "instance_administration_api": {
    "deployment_id": "crn:v1:bluemix:public:dashdb-for-transactions:eu-gb:a/07c1f4be2bb544ba8a0b0417a8b27766:06f2276e-7aff-412f-9e75-0f622f2d4cf4::",
    "instance_id": "crn:v1:bluemix:public:dashdb-for-transactions:eu-gb:a/07c1f4be2bb544ba8a0b0417a8b27766:06f2276e-7aff-412f-9e75-0f622f2d4cf4::",
    "root": "https://apieugb.db2.cloud.ibm.com/v5/ibm"
  }
}
'''
conn_str='database=bludb;hostname=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;port=32328;protocol=tcpip;\
        uid=mgc79809;pwd=JSAP0x7FXgDIo30t;security=SSL'
ibm_db_conn = ibm_db.connect(conn_str,'','')
    
print("Database connected without any error !!")
# except:
    # print("IBM DB Connection error   :     " )    #+ DB2.conn_errormsg()

# app.config['']

# mysql = MySQL(app)


#HOME--PAGE
@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")



#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    print("Break point1")
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        print("Break point2" + "name: " + username + "------" + email + "------" + password)

        try:
            print("Break point3")
            connectionID = ibm_db_dbi.connect(conn_str, '', '')
            cursor = connectionID.cursor()
            print("Break point4")
        except:
            print("No connection Established")      

        # cursor = mysql.connection.cursor()
        # with app.app_context():
        #     print("Break point3")
        #     cursor = ibm_db_conn.cursor()
        #     print("Break point4")
        
        print("Break point5")
        sql = "SELECT * FROM register WHERE username = ?"
        stmt = ibm_db.prepare(ibm_db_conn, sql)
        print(username)
        ibm_db.bind_param(stmt, 1, 50)
        ibm_db.execute(stmt)
        result = ibm_db.execute(stmt)
        print(result)
        account = ibm_db.fetch_row(stmt)
        print(account)

        param = "SELECT * FROM register WHERE username = " + "\'" + username + "\'"
        res = ibm_db.exec_immediate(ibm_db_conn, param)
        print("---- ")
        dictionary = ibm_db.fetch_assoc(res)
        while dictionary != False:
            print("The ID is : ", dictionary["USERNAME"])
            dictionary = ibm_db.fetch_assoc(res)

        # dictionary = ibm_db.fetch_assoc(result)
        # cursor.execute(stmt)

        # account = cursor.fetchone()
        # print(account)

        # while ibm_db.fetch_row(result) != False:
        #     # account = ibm_db.result(stmt)
        #     print(ibm_db.result(result, "username"))

        # print(dictionary["username"])    
        print("break point 6")
        if account:
            msg = 'Username already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            sql2 = "INSERT INTO register (username, email,password,id) VALUES (?, ?, ?,?)"
            stmt2 = ibm_db.prepare(ibm_db_conn, sql2)
            ibm_db.bind_param(stmt2, 1, username)
            ibm_db.bind_param(stmt2, 2, email)
            ibm_db.bind_param(stmt2, 3, password)
            ibm_db.bind_param(stmt2, 4, email)
            ibm_db.execute(stmt2)
            # cursor.execute('INSERT INTO register VALUES (NULL, % s, % s, % s)', (username, email,password))
            # mysql.connection.commit()
            msg = 'You have successfully registered !'
        return render_template('signup.html', msg = msg)
        
        
 
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password ),)
        # account = cursor.fetchone()
        # print (account)
        
        sql = "SELECT * FROM register WHERE username = ? and password = ?"
        stmt = ibm_db.prepare(ibm_db_conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        result = ibm_db.execute(stmt)
        print(result)
        account = ibm_db.fetch_row(stmt)
        print(account)
        
        param = "SELECT * FROM register WHERE username = " + "\'" + username + "\'" + " and password = " + "\'" + password + "\'"
        res = ibm_db.exec_immediate(ibm_db_conn, param)
        dictionary = ibm_db.fetch_assoc(res)

        # sendmail("hello sakthi","sivasakthisairam@gmail.com")

        if account:
            session['loggedin'] = True
            session['id'] = dictionary["ID"]
            userid = dictionary["ID"]
            session['username'] = dictionary["USERNAME"]
            session['email'] = dictionary["EMAIL"]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
        
    return render_template('login.html', msg = msg)



       





#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']

    print(date)
    p1 = date[0:10]
    p2 = date[11:13]
    p3 = date[14:]
    p4 = p1 + "-" + p2 + "." + p3 + ".00"
    print(p4)
    # cursor = mysql.connection.cursor()
    # cursor.execute('INSERT INTO expenses VALUES (NULL,  % s, % s, % s, % s, % s, % s)', (session['id'] ,date, expensename, amount, paymode, category))
    # mysql.connection.commit()
    # print(date + " " + expensename + " " + amount + " " + paymode + " " + category)

    sql = "INSERT INTO expenses (userid, date, expensename, amount, paymode, category) VALUES (?, ?, ?, ?, ?, ?)"
    stmt = ibm_db.prepare(ibm_db_conn, sql)
    print("Session id is"+session['id'])
    ibm_db.bind_param(stmt, 1, session['id'])
    ibm_db.bind_param(stmt, 2, p4)
    ibm_db.bind_param(stmt, 3, expensename)
    ibm_db.bind_param(stmt, 4, amount)
    ibm_db.bind_param(stmt, 5, paymode)
    ibm_db.bind_param(stmt, 6, category)
    ibm_db.execute(stmt)

    print("Expenses added")

    # email part

    param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " AND MONTH(date) = MONTH(current timestamp) AND YEAR(date) = YEAR(current timestamp) ORDER BY date DESC"
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    expense = []
    while dictionary != False:
        temp = []
        temp.append(dictionary["ID"])
        temp.append(dictionary["USERID"])
        temp.append(dictionary["DATE"])
        temp.append(dictionary["EXPENSENAME"])
        temp.append(dictionary["AMOUNT"])
        temp.append(dictionary["PAYMODE"])
        temp.append(dictionary["CATEGORY"])
        expense.append(temp)
        print(temp)
        dictionary = ibm_db.fetch_assoc(res)

    total=0
    for x in expense:
          total += x[4]

    param = "SELECT id, limitss FROM limits WHERE userid = " + str(session['id']) + " ORDER BY id DESC LIMIT 1"
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    row = []
    s = 0
    while dictionary != False:
        temp = []
        temp.append(dictionary["LIMITSS"])
        row.append(temp)
        dictionary = ibm_db.fetch_assoc(res)
        s = temp[0]

    if total > int(s):
        msg = "Hello " + session['username'] + " , " + "you have crossed the monthly limit of Rs. " + s + "/- !!!" + "\n" + "Thank you, " + "\n" + "Team Personal Expense Tracker."  
        sendmail(msg,session['email'])  
    
    return redirect("/display")



#DISPLAY---graph 

@app.route("/display")
def display():
    print(session["username"],session['id'])
    
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM expenses WHERE userid = % s AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    # expense = cursor.fetchall()

    param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " ORDER BY date DESC"
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    expense = []
    while dictionary != False:
        temp = []
        temp.append(dictionary["ID"])
        temp.append(dictionary["USERID"])
        temp.append(dictionary["DATE"])
        temp.append(dictionary["EXPENSENAME"])
        temp.append(dictionary["AMOUNT"])
        temp.append(dictionary["PAYMODE"])
        temp.append(dictionary["CATEGORY"])
        expense.append(temp)
        print(temp)
        dictionary = ibm_db.fetch_assoc(res)

    return render_template('display.html' ,expense = expense)
                          



#delete---the--data

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
    #  cursor = mysql.connection.cursor()
    #  cursor.execute('DELETE FROM expenses WHERE  id = {0}'.format(id))
    #  mysql.connection.commit()

    param = "DELETE FROM expenses WHERE  id = " + id
    res = ibm_db.exec_immediate(ibm_db_conn, param)

    print('deleted successfully')    
    return redirect("/display")
 
    
#UPDATE---DATA

@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM expenses WHERE  id = %s', (id,))
    # row = cursor.fetchall()

    param = "SELECT * FROM expenses WHERE  id = " + id
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    row = []
    while dictionary != False:
        temp = []
        temp.append(dictionary["ID"])
        temp.append(dictionary["USERID"])
        temp.append(dictionary["DATE"])
        temp.append(dictionary["EXPENSENAME"])
        temp.append(dictionary["AMOUNT"])
        temp.append(dictionary["PAYMODE"])
        temp.append(dictionary["CATEGORY"])
        row.append(temp)
        print(temp)
        dictionary = ibm_db.fetch_assoc(res)

    print(row[0])
    return render_template('edit.html', expenses = row[0])




@app.route('/update/<id>', methods = ['POST'])
def update(id):
  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
    
    #   cursor = mysql.connection.cursor()
    #   cursor.execute("UPDATE `expenses` SET `date` = % s , `expensename` = % s , `amount` = % s, `paymode` = % s, `category` = % s WHERE `expenses`.`id` = % s ",(date, expensename, amount, str(paymode), str(category),id))
    #   mysql.connection.commit()

      p1 = date[0:10]
      p2 = date[11:13]
      p3 = date[14:]
      p4 = p1 + "-" + p2 + "." + p3 + ".00"

      sql = "UPDATE expenses SET date = ? , expensename = ? , amount = ?, paymode = ?, category = ? WHERE id = ?"
      stmt = ibm_db.prepare(ibm_db_conn, sql)
      ibm_db.bind_param(stmt, 1, p4)
      ibm_db.bind_param(stmt, 2, expensename)
      ibm_db.bind_param(stmt, 3, amount)
      ibm_db.bind_param(stmt, 4, paymode)
      ibm_db.bind_param(stmt, 5, category)
      ibm_db.bind_param(stmt, 6, id)
      ibm_db.execute(stmt)

      print('successfully updated')
      return redirect("/display")
     
      

            
 
         
    
            
 #limit
@app.route("/limit" )
def limit():
       return redirect('/limitn')

@app.route("/limitnum" , methods = ['POST' ])
def limitnum():
     if request.method == "POST":
         number= request.form['number']
        #  cursor = mysql.connection.cursor()
        #  cursor.execute('INSERT INTO limits VALUES (NULL, % s, % s) ',(session['id'], number))
        #  mysql.connection.commit()

         sql = "INSERT INTO limits (userid, limitss) VALUES (?, ?)"
         stmt = ibm_db.prepare(ibm_db_conn, sql)
         ibm_db.bind_param(stmt, 1, session['id'])
         ibm_db.bind_param(stmt, 2, number)
         ibm_db.execute(stmt)
         
         return redirect('/limitn')
     
         
@app.route("/limitn") 
def limitn():
    # cursor = mysql.connection.cursor()
    # cursor.execute('SELECT limitss FROM `limits` ORDER BY `limits`.`id` DESC LIMIT 1')
    # x= cursor.fetchone()
    # s = x[0]
    
    param = "SELECT id, limitss FROM limits WHERE userid = " + str(session['id']) + " ORDER BY id DESC LIMIT 1"
    res = ibm_db.exec_immediate(ibm_db_conn, param)
    dictionary = ibm_db.fetch_assoc(res)
    row = []
    s = " /-"
    while dictionary != False:
        temp = []
        temp.append(dictionary["LIMITSS"])
        row.append(temp)
        dictionary = ibm_db.fetch_assoc(res)
        s = temp[0]
    
    return render_template("limit.html" , y= s)

#REPORT

@app.route("/today")
def today():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT TIME(date)   , amount FROM expenses  WHERE userid = %s AND DATE(date) = DATE(NOW()) ',(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)

      param1 = "SELECT TIME(date) as tn, amount FROM expenses WHERE userid = " + str(session['id']) + " AND DATE(date) = DATE(current timestamp) ORDER BY date DESC"
      res1 = ibm_db.exec_immediate(ibm_db_conn, param1)
      dictionary1 = ibm_db.fetch_assoc(res1)
      texpense = []

      while dictionary1 != False:
          temp = []
          temp.append(dictionary1["TN"])
          temp.append(dictionary1["AMOUNT"])
          texpense.append(temp)
          print(temp)
          dictionary1 = ibm_db.fetch_assoc(res1)
      
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    #   expense = cursor.fetchall()

      param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " AND DATE(date) = DATE(current timestamp) ORDER BY date DESC"
      res = ibm_db.exec_immediate(ibm_db_conn, param)
      dictionary = ibm_db.fetch_assoc(res)
      expense = []
      while dictionary != False:
          temp = []
          temp.append(dictionary["ID"])
          temp.append(dictionary["USERID"])
          temp.append(dictionary["DATE"])
          temp.append(dictionary["EXPENSENAME"])
          temp.append(dictionary["AMOUNT"])
          temp.append(dictionary["PAYMODE"])
          temp.append(dictionary["CATEGORY"])
          expense.append(temp)
          print(temp)
          dictionary = ibm_db.fetch_assoc(res)

  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
     

@app.route("/month")
def month():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= %s AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) ',(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)

      param1 = "SELECT DATE(date) as dt, SUM(amount) as tot FROM expenses WHERE userid = " + str(session['id']) + " AND MONTH(date) = MONTH(current timestamp) AND YEAR(date) = YEAR(current timestamp) GROUP BY DATE(date) ORDER BY DATE(date)"
      res1 = ibm_db.exec_immediate(ibm_db_conn, param1)
      dictionary1 = ibm_db.fetch_assoc(res1)
      texpense = []

      while dictionary1 != False:
          temp = []
          temp.append(dictionary1["DT"])
          temp.append(dictionary1["TOT"])
          texpense.append(temp)
          print(temp)
          dictionary1 = ibm_db.fetch_assoc(res1)
      
      
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND MONTH(DATE(date))= MONTH(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    #   expense = cursor.fetchall()

      param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " AND MONTH(date) = MONTH(current timestamp) AND YEAR(date) = YEAR(current timestamp) ORDER BY date DESC"
      res = ibm_db.exec_immediate(ibm_db_conn, param)
      dictionary = ibm_db.fetch_assoc(res)
      expense = []
      while dictionary != False:
          temp = []
          temp.append(dictionary["ID"])
          temp.append(dictionary["USERID"])
          temp.append(dictionary["DATE"])
          temp.append(dictionary["EXPENSENAME"])
          temp.append(dictionary["AMOUNT"])
          temp.append(dictionary["PAYMODE"])
          temp.append(dictionary["CATEGORY"])
          expense.append(temp)
          print(temp)
          dictionary = ibm_db.fetch_assoc(res)

  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
         
@app.route("/year")
def year():
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= %s AND YEAR(DATE(date))= YEAR(now()) GROUP BY MONTH(date) ORDER BY MONTH(date) ',(str(session['id'])))
    #   texpense = cursor.fetchall()
    #   print(texpense)

      param1 = "SELECT MONTH(date) as mn, SUM(amount) as tot FROM expenses WHERE userid = " + str(session['id']) + " AND YEAR(date) = YEAR(current timestamp) GROUP BY MONTH(date) ORDER BY MONTH(date)"
      res1 = ibm_db.exec_immediate(ibm_db_conn, param1)
      dictionary1 = ibm_db.fetch_assoc(res1)
      texpense = []

      while dictionary1 != False:
          temp = []
          temp.append(dictionary1["MN"])
          temp.append(dictionary1["TOT"])
          texpense.append(temp)
          print(temp)
          dictionary1 = ibm_db.fetch_assoc(res1)
      
      
    #   cursor = mysql.connection.cursor()
    #   cursor.execute('SELECT * FROM expenses WHERE userid = % s AND YEAR(DATE(date))= YEAR(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
    #   expense = cursor.fetchall()

      param = "SELECT * FROM expenses WHERE userid = " + str(session['id']) + " AND YEAR(date) = YEAR(current timestamp) ORDER BY date DESC"
      res = ibm_db.exec_immediate(ibm_db_conn, param)
      dictionary = ibm_db.fetch_assoc(res)
      expense = []
      while dictionary != False:
          temp = []
          temp.append(dictionary["ID"])
          temp.append(dictionary["USERID"])
          temp.append(dictionary["DATE"])
          temp.append(dictionary["EXPENSENAME"])
          temp.append(dictionary["AMOUNT"])
          temp.append(dictionary["PAYMODE"])
          temp.append(dictionary["CATEGORY"])
          expense.append(temp)
          print(temp)
          dictionary = ibm_db.fetch_assoc(res)

  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )

#log-out

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('email', None)
   return render_template('home.html')

             
port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)