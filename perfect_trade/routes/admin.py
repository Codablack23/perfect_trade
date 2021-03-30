from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from perfect_trade import mysql
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

def getInfo(query):
    investment=mysql.connection.cursor()
    investment.execute(query)
    data=list(investment.fetchall())
    return data
    investment.close()

def getAdmin(query):
    admin=mysql.connection.cursor()
    admin.execute(query)
    data=list(admin.fetchall())
    return data
    investment.close()

def addPromo(title,duration,description):
    promo=mysql.connection.cursor()
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
    promo.connection.commit()
    data=promo.rowcount
    promo.close()
    return data
  


def deleteAdmin(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"Delete From perfect_trade_adminstrators WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

def suspendAdmin(Id,stats):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE perfect_trade_adminstrators SET Suspended='{stats}' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row


def accept(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE withdrawals SET Status='Accepted' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row
def reject(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE withdrawals SET Status='Rejected' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

def deletePromo(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"Delete From promos WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

def suspendPromo(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE promos SET Status='Suspended' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

def resumePromo(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE promos SET Status='Ongoing' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

def endPromo(Id):
    admin=mysql.connection.cursor()
    admin.execute(f"UPDATE promos SET Status='Ended' WHERE Id ='{Id}'")
    admin.connection.commit()
    row=admin.rowcount
    return row

@app.route("/admin/", methods=["GET", "POST"])
def adminLogin():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        db=mysql.connection.cursor()
        fetch_query=f'SELECT * FROM perfect_trade_adminstrators WHERE Username="{username}"'
        user=db.execute(fetch_query)
        if user > 0:
            admin=db.fetchone()
            db_password=admin['Password']
            if sha256_crypt.verify(password,db_password):
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
    return render_template("Admin/home.html", Page="Dashboard",Clients=clients,withdraws=all_withdraws,investments=all_investments)

@app.route('/admin/withdraws')
@AuthorizeAdmin
def adminWithdraws():
    all_withdraws=getInfo("SELECT * FROM withdrawals")
    return render_template("Admin/withdraws.html", Page="Withdraws", Withdraws=all_withdraws)

@app.route('/admin/clients')
@AuthorizeAdmin
def adminClients():
    account_info=getInfo("SELECT * FROM account_details")
    All_clients=getInfo("SELECT * FROM perfect_trade_users")
    return render_template("Admin/clients.html", Page="Investors",Clients=All_clients,accounts=account_info)

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
        db=mysql.connection.cursor()
        query=f"INSERT INTO perfect_trade_adminstrators(Username, Password, Email,Admin_Name,Superuser,Suspended) VALUES('{username}','{password}','{email}','{name}','{superuser}','{suspended}')"
        db.execute(query)
        db.connection.commit()
        count=db.rowcount
        db.close()
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