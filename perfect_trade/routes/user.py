from flask import Flask, render_template,redirect,logging,flash,url_for,session,request
from perfect_trade import mysql
from perfect_trade import mail
from flask_mail import Message
from perfect_trade import app
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from perfect_trade.forms.signup import SignUpForm
from datetime import datetime
from random import random
from .authorization import Authorize,AuthorizeSignUp,AuthorizePassChange
import json
import threading

@app.route("/signup", methods=["GET", "POST"])
def SignUp():
    form=SignUpForm(request.form)
    date=datetime.now().year
    random_number=int(random()*1000000)
    customer_id=f'salemfx/{date}/{random_number}'

    if request.method=="POST" and form.validate():
        surname=form.surname.data
        firstname=form.firstName.data
        email=form.email.data
        password=sha256_crypt.hash(str(form.password.data))

        

        find_query=f"SELECT * FROM perfect_trade_users WHERE Email= '{email}' OR (Surname='{surname}' AND Firstname='{firstname}')"
        db=mysql.connection.cursor()
        res= db.execute(find_query)
        if res >0:
             db.close()
             flash("User Already Exist", "red")
             redirect(url_for('SignUp'))
        else:
                details={
                'surname':surname,
                'firstname':firstname,
                'email': email,
                'password':  password
                }
                session['details']=details
                raw_pin=int(random()*1000000)
                pin=f'{raw_pin:5}'
                app.logger.info(pin)

                session["pin"]=pin
                msg=Message()
                msg.subject="Email Verification"
                msg.body=f"Your Email Verification Pin is {pin} This Pin Will Expire In Five Minutes"
                msg.recipients=[email]
                msg.sender="goodluckedih@gmail.com"
                try:
                    mail.send(msg)
                    return redirect(url_for("confirm_email"))
    
                except Exception as error:
                    flash("Sorry It Seems an Error Occured", "red")
                    redirect(url_for("SignUp"))
                     
               
     

    return render_template('User/sign_up.html', Page="Sign Up", form=form)

@app.route("/login", methods=["GET", "POST"])
def LogIn():
    if request.method=="POST":
        email=request.form['email']
        recieved_password=request.form['password']
        db=mysql.connection.cursor()
        fetch_query=f'SELECT * FROM perfect_trade_users WHERE Email="{email}"'
        user=db.execute(fetch_query)
        if user > 0:
            data=db.fetchone()
            db_password=data['Password']
            if sha256_crypt.verify(recieved_password,db_password):
                session['logged_in']=True
                session['Email']=email
                return redirect(url_for('Dashboard'))
            else:
                 flash("Password Does Not Match User","red")
                 app.logger.info("PASSWORD INCORRECT")
            db.close()
        else:
            flash("User Does Not Exist","red")

      
    return render_template('User/login.html', Page="Login")

@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotPassword():
        if request.method=="POST":
            email=request.form['email']
            letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
            pin=f"{letters[int(random()*len(letters))]}{int(random()*len(letters))}{letters[int(random()*len(letters))]}{int(random()*len(letters))}{letters[int(random()*len(letters))]}{int(random()*len(letters))}"
            db=mysql.connection.cursor()
            user=db.execute(f"SELECT * FROM perfect_trade_users WHERE Email='{email}'")
            if user > 0:
                session['recovery']=True
                session['recovery_pin']=pin
                session['recovery_email']=email
                new_msg=Message()
                new_msg=Message()
                new_msg.subject="Password Recovery"
                new_msg.body=f"Your Recovery Pin is {pin} Do Not Share Your Pin Use This To Change Your Password"
                new_msg.recipients=[email]
                new_msg.sender="Perfect Trade"
             
                try:
                    mail.send(new_msg)
                    return  redirect(url_for('passwordGenLogin'))
    
                except Exception as error:
                    app.logger.info(error)
                    flash("Sorry It Seems an Error Occured", "red")
            else:
                flash("User Does Not Exist","red")

        return render_template('User/forgot_password.html',Page="Forgot Password")

@app.route("/clearsession", methods=["GET", "POST"])
@AuthorizeSignUp
def clearSession():
    if request.method =="POST":
       del(session['pin'])
       del(session['details'])
       status={
           "message":"Session Cleared"
       }
       return json.dumps(status)


def clear():
     del(session['pin'])
     del(session['details'])

@app.route("/confirm_email", methods=["GET", "POST"])
@AuthorizeSignUp
def confirm_email():
      response={
         "status":""
      }
      if request.method=="POST":
        db=mysql.connection.cursor()
        info=dict(request.form)
        user_pin=info['pin']

        details=session['details']

        firstname=details['firstname']   
        surname=details['surname']    
        email=details['email']
        password=sha256_crypt.encrypt(details['password'])
        customer_id=['customer_id']

        add_query=f'INSERT INTO perfect_trade_users(Firstname, Surname, Email, Password, Customer_ID) VALUES("{firstname}","{surname}","{email}","{password}","{customer_id}")'     
        add_query=f'INSERT INTO account(Name, Email, Balance,Currency) VALUES("{firstname+surname}","{email}","{0.00}","USD")'    
        if user_pin == session['pin']:
             db.execute(add_query)
             db.connection.commit()
             count=db.rowcount
             db.close()
            #  flash("You Have Registered Sucessfully You can Now Login ", "green")
             if count > 0:
                del(session['details'])
                del(session['pin'])
                response['status']="success"
             else:
                response['status']="success"
             return json.dumps(response)
        
        

        else:
            #  flash("Your Pin Do Not Match ", "red")
             response['status']="failed"
            #  redirect(url_for('confirm_email'))
             return json.dumps(response) 

    #   timer=threading.Timer(int(60*5),clear())
    #   timer.start()
      return render_template('User/confirm_email.html',Page="Confirm Email")


@app.route("/rlogin", methods=['GET', 'POST'])
@AuthorizePassChange
def passwordGenLogin():
    new_message={
        "message":"",
        "color":""

        }
    if request.method=="POST":
        data=dict(request.form)
        email=session['recovery_email']
        pin=data['r_pin']
        new_password=data['new_password']
        confirmed=data['confirm_password']
        db=mysql.connection.cursor()

        if pin == session['recovery_pin']:
            if confirmed == new_password:
                updated_password=sha256_crypt.encrypt(new_password)
                db.execute(f'UPDATE perfect_trade_users SET Password="{updated_password}" WHERE Email="{email}" ')
                db.connection.commit()
                count = db.rowcount
                if count > 0:
                    new_message['message']=f"You have successfully Changed Your Password  Your New Password is '{new_password}' Please Do Not Share with Anyone"
                    new_message['color']="green"
                    del(session['recovery'])
                    del(session['recovery_pin'])
                    del(session['recovery_email'])
                else:
                    flash("An Error Has Occured","red")
            
            else:
                 flash("Passwords Do Not Match","red")
        else:
            flash("Incorrect Pin","red")
        db.close()
    return render_template('User/fp_login.html', Page="Recovery Login",message=new_message)

