from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from perfect_trade import host,db as dbs,password,port,user as hostuser,charset
from perfect_trade import app
from .authorization import Authorize
from datetime import datetime
import pymysql
from perfect_trade import mail
from flask_mail import Message
import pymysql.cursors

def addInvestment(name,email,duration,amount,currency,plan,returns,percent,payment_stats):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    promo=mysql.cursor(pymysql.cursors.DictCursor)
    status="Ongoing"
    percentage=percent
    current_day=datetime.now().day
    day_index=int(duration)%30
    end_day=current_day + day_index
    month_index=int(duration)//30
    end_month=datetime.now().month + month_index
    end_year=datetime.now().year
    if end_month > 12:
        endmonth -=12
        end_year +=1
    if end_day > 30:
        end_day-=30
    end_date=datetime(end_year, end_month, end_day)
    
    query=f"INSERT INTO investments(Name,Duration_Days,Amount,Status,Date_Of_Returns,Percentage,Plan,Currency,Email,Amount_Recieved,Payment_Status) VALUES('{name}','{duration}','{amount}','{status}','{end_date}','{percentage}','{plan}','{currency}','{email}','{returns}','{payment_stats}')"
    promo.execute(query)
    mysql.commit()
    data=promo.rowcount
    mysql.close()
    return data

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
    mysql.close()

def getinvestments():
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    db=mysql.cursor(pymysql.cursors.DictCursor)
    db.execute(f'SELECT * FROM investments WHERE Email="{session["Email"]}"')
    data=db.fetchall()
    return data

def getAccountDetails():
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    user_data=mysql.cursor(pymysql.cursors.DictCursor)
    user_data.execute(f"SELECT * FROM account_details WHERE Email='{session['Email']}'")
    data=user_data.fetchone()
    return data
    user_data.close()

def getAccount(email):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    user_data=mysql.cursor(pymysql.cursors.DictCursor)
    data= user_data.execute(f"SELECT * FROM account_details WHERE Email='{email}'")
    return data
    user_data.close()

def endInvestment(Id,status):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    connect =mysql.cursor(pymysql.cursors.DictCursor)
    query=f"UPDATE investments SET Status='{status}' WHERE Id='{Id}'"
    connect.execute(query)
    mysql.commit()
    count=connect.rowcount
    mysql.close


@app.route("/dashboard/")
@Authorize
def Dashboard():
    user=getUserData()
    current_date=datetime.now().strftime("%x")
    investments=getinvestments()
    ongoing=[]
    Completed=[]
    for investment in investments:
        if  current_date > investment['Date_Of_Returns'].strftime("%x") :
            endInvestment(investment['Id'],'Completed')
        else:
            endInvestment(investment['Id'],'Ongoing')
    fullname=f"{user['Firstname']} {user['Surname']}"
    for invest in investments:
        if invest['Status']=="Ongoing" and invest['Payment_Status']=="Paid":
            ongoing.append(invest)
        else:
            if invest['Status']=="Completed":
               Completed.append(invest)
  
    ongoingLength=len(ongoing)
    completedLength=len(Completed)
    return render_template("Dashboard/home.html", Page="Home", fullname=fullname,Ongoing=ongoing,complete=Completed,onlength=ongoingLength,compLength=completedLength)

@app.route("/dashboard/logout")
@Authorize
def logout():
    session.clear()
    flash("You Have Logged out", "green")
    return redirect(url_for("LogIn"))


# @app.route("/dashboard/referrals")
# @Authorize
# def referrals():
#     user=getUserData()
#     fullname=f"{user['Firstname']} {user['Surname']}"
#     return render_template('Dashboard/referrals.html', Page="Referrals", fullname=fullname, user=user)


@app.route("/dashboard/invest",methods=["GET","POST"])
@Authorize
def invest():
    user=getUserData()
    fullname=f"{user['Firstname']} {user['Surname']}"
    if request.method=='POST':
      status={
          "Success":False
      }
      data=dict(request.form)
      amount=data['amount']
      returns=data['returns']
      currency=data['currency']
      new_email=data['email']
      duration=data['Duration']
      plan=data['plan']
      percent=data['percent']
      payment_stats="Not Paid"
      new_investment=addInvestment(fullname,new_email,duration,amount,currency,plan,returns,percent,payment_stats)
      if new_investment > 0:
          status['Success']=True
          new_msg=Message()
          new_msg.subject="Starting Investment"
          new_msg.body=f'{fullname} from Perfect Trade is About To Make an Investment Of {amount} {currency} through the BTC or Etherum Address You will Recieve A Payment Soon'
          new_msg.recipients=['perfecttrades.com@gmail.com']
          new_msg.sender=f'{fullname} From Perfect Trade'
          mail.send(new_msg)  
      else :
          status['Success']=False
          status['error']="An Error Occured"
      return jsonify(status)
    return render_template('Dashboard/invest.html', Page="Invest", fullname=fullname, user=user)

@app.route("/dashboard/withdrawals")
@Authorize
def withdrawal():
    user=getUserData()
    fullname=f"{user['Firstname']} {user['Surname']}"
    return render_template('Dashboard/withdrawal.html', Page="Withdrawals", fullname=fullname, user=user)


@app.route("/dashboard/accounts", methods=['GET','POST'])
@Authorize
def accounts():
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    if request.method=="POST":
        stats={
          "Success":""
        }
       
        db=mysql.cursor(pymysql.cursors.DictCursor)
        data=request.form
        account_number=data['account_number']
        account_name=data['account_name']
        bank=data['bank']
        country=data['country']
        email=session["Email"]
        check=getAccount(email)
        if check > 0:
            
            db.execute(f"UPDATE account_details SET Name='{account_name}', Account_No='{account_number}',Bank='{bank}' WHERE Email='{session['Email']}'")
            mysql.commit()
            count=db.rowcount
            if count >0:
                stats["Success"]="True"
            else:
                stats["Success"]="True"
                stats["Error"]="An Error Has Occured"
        else:
            query=f"INSERT INTO account_details (Name,Account_No,Bank,Email,Account_Name) VALUES('{account_name}','{account_number}','{bank}','{email}','{account_name}')"
            db.execute(query)
            mysql.commit()
            count=db.rowcount
            if count >0:
                stats["Success"]="True"
            else:
                stats["Success"]="True"
                stats["Error"]="An Error Has Occured"
                app.logger.info(db.connection.error)
        mysql.close()
        return jsonify(stats)
    user_data=mysql.cursor(pymysql.cursors.DictCursor)
    user=getUserData()
    mylist= user_data.execute(f"SELECT * FROM account_details WHERE Email='{session['Email']}'")
    data=""
    length=False
    if mylist>0:
        data=user_data.fetchone()
        mysql.close()
        length=True
    else:
        length=False
    fullname=f"{user['Firstname']} {user['Surname']}"
    return render_template('Dashboard/accounts.html', Page="Accounts", fullname=fullname, user=user,accounts=data,L=length)

@app.route("/dashboard/charts")
@Authorize
def charts():
    user=getUserData()
    fullname=f"{user['Firstname']} {user['Surname']}"
    return render_template('Dashboard/charts.html', Page="Charts", fullname=fullname, user=user)

@app.route("/dashboard/api_keys", methods=["POST"])
@Authorize
def getApi():
    apis={
      "public_key": 'pk_live_c354c6e98a480c1374b6da9544dbab6f83f5ffa4',
      "api_key":'22e8c7fda4cc950b8a9f'
    }
    return jsonify(apis)


@app.route("/dashboard/changepassword",methods=["POST","GET"])
@Authorize
def changePassword():
    user=getUserData()
    fullname=f"{user['Firstname']} {user['Surname']}"
    if request.method=="POST":
        email=session['Email']
        old_password=request.form['old_password']
        new_password=request.form['new_password']
        if sha256_crypt.verify(old_password,user['Password']):
            updated_password=sha256_crypt.encrypt(new_password)
            mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
            db=mysql.cursor(pymysql.cursors.DictCursor)
            db.execute(f'UPDATE perfect_trade_users SET Password="{updated_password}" WHERE Email="{email}" ')
            mysql.commit()
            flash(f"You have successfully Changed Your Password  Your New Password is '{new_password}' Please Do Not Share with Anyone","green")

            redirect(url_for('changePassword'))
        
        else:
            flash("Old Password Does Not Match ","red")

    

    return render_template('Dashboard/change_password.html', Page="Change Password", fullname=fullname, user=user)