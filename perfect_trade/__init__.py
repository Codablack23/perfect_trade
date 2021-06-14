from flask import Flask
# from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

# class MysqlConnection(object):
#     def __init__(self):
#         self.host ="mysql-26183-0.cloudclusters.net"
#         self.port = 26183
#         self.user = 'perfect_trades'
#         self.passwd = 'perfect-trade'
#         self.db = 'perfect_trade_db'

#     def connect_mysql(self):
#         return pymysql.Connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)

#     def operate_database(self):
#         # example select mysql version
#         connect = self.connect_mysql()
#         cursor = connect.cursor()
#         cursor.execute("SELECT VERSION()")
#         data = cursor.fetchone()
#         print('version is :', data[0])
#         connect.close()

app = Flask(__name__)
app.secret_key="b'bV/\x1d\xc1\xf9\x96i\x15\xaa\xe9\x85A\xb0+Y\x11&\x111cz?+'"
host="mysql-34058-0.cloudclusters.net"
port=34058
user="perfect_trade"
password="perfect_trade"
db='perfect_trade'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///mydb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

database=SQLAlchemy(app)
ma=Marshmallow(app)
charset='utf8mb4'
# cur=pymysql.cursors.DictCursor
# app.config['MYSQL_HOST']="https://mysql-26183-0.cloudclusters.net"
# app.config['MYSQL_PORT']=26183
# app.config['MYSQL_USER']= "perfect_trade"
# app.config['MYSQL_PASSWORD']= "perfect_trade"
# app.config['MYSQL_DB']="perfect_trade_db"
# app.config['MYSQL_CURSORCLASS'] ="DictCursor"


# MysqlConnection().operate_database()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "perfecttrades.com.ng@gmail.com"
app.config['MAIL_PASSWORD'] = "perfecttrades@password.com"
mail = Mail(app)

from .models import Users,messages,account,account_details,Promo,investments,withdrawals,Admin,wallet

from .routes import home
from .routes import users
from .routes import dashboard
from .routes import dashboard_api
from .routes import admin
from .routes import training
