from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from perfect_trade import host,db as dbs,password,port,user as hostuser,charset
from perfect_trade import mail
from flask_mail import Message
from perfect_trade import app
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from perfect_trade.forms.signup import SignUpForm
from datetime import datetime
from random import random
from .authorization import AuthorizeAdmin
import json
import threading
import pymysql
import pymysql.cursors

def getInfo(query):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    investment=mysql.cursor(pymysql.cursors.DictCursor)
    investment.execute(query)
    data=list(investment.fetchall())
    return data
    mysql.close()
    
    

def confirm_investment(Id):
    date=datetime.now()
    current_day=datetime.now().day
    duration=7*30
    day_index=int(duration)%30
    end_day=current_day + int(day_index)
    month_index=int(duration)//30
    end_month=datetime.now().month + month_index
    end_year=datetime.now().year
    if end_month > 12:
        endmonth -=12
        end_year += endmonth-12
    if end_day > 30:
        end_day-=30
  
    end_date=datetime(end_year, end_month, end_day)
    query=f'UPDATE investments SET Payment_Status="Paid",Date_Invested="{date}",Date_Of_Returns="{end_date}" WHERE Id="{Id}"'
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    investment=mysql.cursor(pymysql.cursors.DictCursor)
    investment.execute(query)
    mysql.commit()
    data=investment.rowcount
    return data
    mysql.close()

def getAdmin(query):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(query)
    data=list(admin.fetchall())
    return data
    mysql.close()

def addPromo(title,duration,description):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    promo=mysql.cursor(pymysql.cursors.DictCursor)
    status="Ongoing"
    current_day=datetime.now().day
    day_index=int(duration)%30
    end_day=current_day + int(day_index)
    month_index=int(duration)//30
    end_month=datetime.now().month + month_index
    end_year=datetime.now().year
    if end_month > 12:
        endmonth -=12
        end_year += endmonth-12
    if end_day > 30:
        end_day-=30
  
    end_date=datetime(end_year, end_month, end_day)
    
    query=f"INSERT INTO promos(Promo_Name,Duration_in_Days,Description,Status,Date_to_End) VALUES('{title}','{duration}','{description}','{status}','{end_date}')"
    promo.execute(query)
    mysql.commit()
    data=promo.rowcount
    mysql.close()
    return data
  


def deleteAdmin(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"Delete From perfect_trade_adminstrators WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row

def suspendAdmin(Id,stats):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE perfect_trade_adminstrators SET Suspended='{stats}' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row


def accept(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE withdrawals SET Status='Accepted' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row
def reject(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE withdrawals SET Status='Rejected' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row

def deletePromo(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"Delete From promos WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row
def getWallets(wallet_type):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    user_data=mysql.cursor(pymysql.cursors.DictCursor)
    user_data.execute(f"SELECT * FROM crypto_wallet WHERE  Wallet_Type='{wallet_type}'")
    data=user_data.fetchall()
    mysql.close()
    return data
    
def suspendPromo(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE promos SET Status='Suspended' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row

def resumePromo(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE promos SET Status='Ongoing' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row

def endPromo(Id):
    mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
    admin=mysql.cursor(pymysql.cursors.DictCursor)
    admin.execute(f"UPDATE promos SET Status='Ended' WHERE Id ='{Id}'")
    mysql.commit()
    row=admin.rowcount
    return row

@app.route("/admin/", methods=["GET", "POST"])
def adminLogin():
    if request.method=="POST":
        username=request.form['username']
        passwords=request.form['password']
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=hostuser,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor(pymysql.cursors.DictCursor)
        fetch_query=f'SELECT * FROM perfect_trade_adminstrators WHERE Username="{username}"'
        user=db.execute(fetch_query)
        if user > 0:
            admin=db.fetchone()
            db_password=admin['Password']
            if sha256_crypt.verify(passwords,db_password):
                session['admin']=True
                session['username']=username
                # return redirect(url_for('Dashboard'))
                return redirect('dashboard')
            else:
                 flash("Password Does Not Match","red")
            db.close()
        else:
            flash("Unauthorized Access","red")

    if 'admin' in session:
        return redirect('dashboard')
    return render_template('Admin/login.html', Page="Admin Login")
@app.route('/admin/dashboard')
@AuthorizeAdmin
def AdminDashboard():
    clients=getInfo("SELECT * FROM perfect_trade_users")
    all_withdraws=getInfo("SELECT * FROM withdrawals") 
    all_investments=getInfo("SELECT * FROM investments")
    all_length=len(all_withdraws)
    i_length=len(all_investments)
    return render_template("Admin/home.html", Page="Dashboard",Clients=clients,withdraws=all_withdraws,investments=all_investments,length=all_length,ln=i_length)

@app.route('/admin/withdraws')
@AuthorizeAdmin
def adminWithdraws():
    all_withdraws=getInfo("SELECT * FROM withdrawals")
    return render_template("Admin/withdraws.html", Page="Withdraws", Withdraws=all_withdraws)

@app.route('/admin/clients')
@AuthorizeAdmin
def adminClients():
    account_info=getInfo("SELECT * FROM account_details")
    btc_wallet=getWallets("BTC")
    eth_wallet=getWallets("ETHERUM")
    All_clients=getInfo("SELECT * FROM perfect_trade_users")
    app.logger.info(btc_wallet)
    app.logger.info(eth_wallet)
    return render_template("Admin/clients.html", Page="Investors",Clients=All_clients,accounts=account_info,btc=btc_wallet,etherum=eth_wallet)

@app.route('/admin/investments')
@AuthorizeAdmin
def adminInvestments():
    all_investments=getInfo("SELECT * FROM investments")
    return render_template("Admin/investments.html", Page="Investments", Investments=all_investments)

@app.route('/admin/admins',methods=["GET","POST"])
@AuthorizeAdmin
def administrators():

    admins=getInfo("SELECT * FROM perfect_trade_adminstrators")
    return render_template("Admin/admins.html", Page="Administrators",Admins=admins)

@app.route('/admin/promo', methods=['GET','POST'])
@AuthorizeAdmin
def promo():
    if request.method=="POST":
        stats={
            "Success":"False"
        }
        data=dict(request.form)
        count=addPromo(data["title"],data['duration'],data['description'])
        if count >0:
            stats['Success']="True"
        else:
            stats["Success"]='False'
            stats['Error']="Couldn't Upload promo Please Check Your Internet Settings"
        return jsonify(stats)
    promos=getInfo("SELECT * FROM promos")
    return render_template("Admin/promo.html", Page="Administrators", Promos=promos)

@app.route("/admin/addAdmin", methods=["POST"])
def addAdmin():
 stats={
     "Success":""
 }
 if request.method=="POST":
    count=0
    data=dict(request.form)
    name=data['name']
    username=f"admin/salemfx/{data['username']}"
    email=data['email']
    new_data=getAdmin(f"SELECT Username FROM perfect_trade_adminstrators Where Username='{username}' OR Email='{email}'")
    pa=data['password']
    superuser="False"
    suspended="False"
    app.logger.info(new_data)
    if len(new_data) < 1:
        password=sha256_crypt.encrypt(str(pa))
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=userhost,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor(pymysql.cursors.DictCursor)
        query=f"INSERT INTO perfect_trade_adminstrators(Username, Password, Email,Admin_Name,Superuser,Suspended) VALUES('{username}','{password}','{email}','{name}','{superuser}','{suspended}')"
        db.execute(query)
        mysql.commit()
        count=db.rowcount
        mysql.close()
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
    else:
        stats["Success"]="False"
        stats["Error"]="Admin Already Exist"

 return jsonify(stats)



@app.route("/admin/deleteAdmin", methods=["POST"])
def deleteAdministrator():
    stats={
      "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=deleteAdmin(data['id'])
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)


@app.route("/admin/suspendAdmin", methods=["POST"])
def suspendAdministrator():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=suspendAdmin(data['id'],"True")
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)


@app.route("/admin/ResumeAdmin", methods=["POST"])
def ResumeAdministrator():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=suspendAdmin(data['id'],"False")
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)

@app.route("/admin/deletePromo", methods=["POST"])
def deletePromos():
    stats={
      "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=deletePromo(data['id'])
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)


@app.route("/admin/suspendPromo", methods=["POST"])
def suspendPromos():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=suspendPromo(data['id'])
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)

@app.route("/admin/resumePromo", methods=["POST"])
def resumePromos():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=resumePromo(data['id'])
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)

@app.route("/admin/endPromo", methods=["POST"])
def endPromos():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=endPromo(data['id'])
        if count > 0:
            stats["Success"]="True"
        else:
            stats["Success"]="False"
        
    return jsonify(stats)

@app.route("/admin/investment.confirmation", methods=["POST"])
def confirmInvestmentPayment(): 
    stats={
        "Success":""
    }
    if request.method=="POST":
        i_id=request.form['id']
        confirm=confirm_investment(i_id)
        if confirm > 0:
            stats['Success']="True"
        else:
             stats['Success']="False"
    return jsonify(stats)

        

@app.route("/admin/accept", methods=["POST"])
def acceptWithdraw():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=accept(data['id'])
        if count > 0:
            stats["Success"]="True"
            new_msg=Message()
            new_msg.subject="Withdrawal Accepted"
            new_msg.body=f"Your withDrawal Of {data['amount']} Requested On {data['date']} Has Been Accepted And Your Account Will Be Credited Soon"
            new_msg.recipients=[data['email']]
            new_msg.sender="Perfect Trade"
            
            try:
                mail.send(new_msg)
                return  redirect(url_for('passwordGenLogin'))

            except Exception as error:
                app.logger.info(error)
                flash("Sorry It Seems an Error Occured", "red")
        else:
            stats["Success"]="False"
        
    return jsonify(stats)

@app.route("/admin/reject", methods=["POST"])
def rejectWthdraw():
    stats={
     "Success":""
    }
    if request.method=="POST":
        data=dict(request.form)
        count=reject(data['id'])
        if count > 0:
            stats["Success"]="True"
            new_msg=Message()
            new_msg.subject="Withdrawal Rejected"
            new_msg.body=f"Your withDrawal Of {data['amount']} Requested On {data['date']} Has Been Rejected Email Us For More Info"
            new_msg.recipients=[data['email']]
            new_msg.sender="Perfect Trade"
            
            try:
                mail.send(new_msg)
                return  redirect(url_for('passwordGenLogin'))

            except Exception as error:
                app.logger.info(error)
                flash("Sorry It Seems an Error Occured", "red")
        else:
            stats["Success"]="False"
        
    return jsonify(stats)