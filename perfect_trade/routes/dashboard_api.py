from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from perfect_trade import host,db as dbs,password,port,user as hostuser,charset
from perfect_trade import app
from .authorization import Authorize
import json
import threading
import datetime
import pymysql
import pymysql.cursors

def getUserData():
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    user_data=mysql.cursor(pymysql.cursors.DictCursor)
    user_data.execute(f"SELECT * FROM perfect_trade_users WHERE Email='{session['Email']}'")
    data=user_data.fetchone()
    return data


@app.route('/request_withdraw',methods=['POST'])
@Authorize
def request_withdraw():
    if request.method == "POST":
        sent_status={
            "status":"Failed"
        }
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        data =dict(request.form)
        amount=data['amount']
        currency=data['currency']
        user=getUserData()
        fullname=f"{user['Firstname']} {user['Surname']}"
        email=session['Email']
        status='Pending'
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"INSERT INTO withdrawals (Name,Email,Amount,Currency,Status) VALUES('{fullname}','{email}','{amount}','{currency}','{status}')"

        db.execute(query)
        mysql.commit()
        db.close()
        sent_status['status']='success'
        return json.dumps(sent_status)


@app.route('/balance',methods=['POST'])
@Authorize
def getBalance():
    if request.method == "POST":
        sent_status={
            "status":"Failed",
            "balance":0.00,
            "currency":"USD"
        }
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        email=session['Email']
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"SELECT * From account WHERE Email='{email}'"

        status=db.execute(query)
        if status>0:
            balance=db.fetchone()
            sent_status['status']='success'
            sent_status['balance']=float(balance['Balance'])
            sent_status['currency']=(balance['Currency'])
            return json.dumps(sent_status)
        else:
            return json.dumps(sent_status)

        mysql.close()

@app.route('/requested_withdraws',methods=['POST'])
@Authorize
def getWithdraws():
    if request.method == "POST":
        withdraw_dict={
            'withdraws':""
        }
        email=session['Email']
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"SELECT * From withdrawals WHERE Email='{email}'"

        status=db.execute(query)
        if status>0:
            info={}
            balance=db.fetchall()
            balance_list=list(balance)
            withdraws=[]
            for bal in balance_list :
              
                app.logger.info(info)

                withdraws.append({
                   'id':bal['Id'],
                   'name':bal['Name'],
                   'email':bal['Email'],
                   'amount':bal['Amount'],
                   'currency':bal['Currency'],
                   'status':bal['Status'],
                   'date':f"{bal['Date'].strftime('%x')}  {bal['Date'].strftime('%X')}"
                })
            withdraw_dict['withdraws']=withdraws
            return jsonify(withdraw_dict)
        else:
            return jsonify(withdraw_dict)

        mysql.close()

@app.route('/account',methods=['POST'])
@Authorize
def getAccounts():
    if request.method == "POST":
        accounts={}
        email=session['Email']
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"SELECT * From account_details WHERE Email='{email}'"

        status=db.execute(query)
        if status>0:
            data=db.fetchone()
            accounts=data
            return json.dumps(accounts)
        else:
            return json.dumps(accounts)

        mysql.close()

@app.route('/investments',methods=['POST'])
@Authorize
def getinvestments():
    if request.method == "POST":
        investment_dict={
            'investments':""
        }
        email=session['Email']
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"SELECT * From investments WHERE Email='{email}'"

        status=db.execute(query)
        if status>0:
            info={}
            balance=db.fetchall()
            investment_list=[]
            for bal in balance:
                info['id']=bal['Id']
                info['name']=bal['Name']
                info['email']=bal['Email']
                info['amount']=bal['Amount']
                info['currency']=bal['Currency']
                info['duration']=bal['Duration_Days']
                info['percentage']=float(bal['Percentage'])
                info['plan']=bal['Plan']
                info['amount_gotten']=bal['Amount_Recieved']
                info['date_invested']=f"{bal['Date_Invested'].strftime('%x')} "
                info['date_of_returns']=f"{bal['Date_Of_Returns'].strftime('%x')}"
                investment_list.append(info)

            investment_dict['investments']=investment_list
            return json.dumps(investment_dict)
        else:
            return json.dumps(investment_dict)

        mysql.close()
