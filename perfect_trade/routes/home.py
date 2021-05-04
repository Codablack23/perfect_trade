from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from perfect_trade import app
from perfect_trade import host,db as dbs,password,port,user as users,charset,database
from perfect_trade import mail
from flask_mail import Message
from perfect_trade.models import Users,new_users
# from perfect_trade.models.schemas import userSchema
import json
import pymysql
@app.route("/",methods=["GET","POST"])
def Landing():
    if request.method == "POST":
        user1= Users('Edih', 'Goodluck', 'goodluckedih@gmail.com', 'my_password', 'my_id')
        database.session.add(user1)
        database.session.commit()

        database_data=Users.query.all()
        return new_users.jsonify(database_data)
    return render_template("index.html", Page="Home")

@app.route("/contact", methods=["POST"])
def contact():
   sat={
       "status":""
   }
   if request.method=="POST":
        mysql=pymysql.connect(host=host,
                      port=port,
                      user=users,
                      password=password,
                      db=dbs,
                      charset=charset,
                      )
        db=mysql.cursor()
        app.logger.info(request.form)
        data=dict(request.form)
      
        # app.logger.info(data)
        email=data["email"]
        firstname=data["firstname"]
        lastname=data["lastname"]
        subject=data["subject"]
        message=data['message']
        query=f"INSERT INTO messages (Email,Message,Firstname,Lastname,Subject) VALUES('{email}','{message}','{firstname}','{lastname}','{subject}')"
        db.execute(query)
        mysql.commit()
        count=db.rowcount
        if count>0:
            sat={
            "status":"success"
            }
            new_msg=Message()
            new_msg.subject=subject
            new_msg.body=message
            new_msg.recipients=['perfecttrades.com@gmail.com']
            new_msg.sender=f'{firstname} {lastname} From Perfect Trade'
            mail.send(new_msg)  
        else:
            sat={
             "status":"Failed"
            }
        mysql.close()
      
       
        return json.dumps(sat)
        
   