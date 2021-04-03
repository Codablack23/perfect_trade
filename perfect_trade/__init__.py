from flask import Flask
# from flask_mysqldb import MySQL
from flask_mail import Mail
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
app.secret_key=os.environ['SECRET_KEY']
secret_key="qwertyuiopasdfghjkl11"
host="mysql-26183-0.cloudclusters.net"
port=26183
user=os.environ['MY_SQL_USERNAME']
password=os.environ['MY_SQL_PASSWORD']
db='perfect_trade_db'
charset='utf8mb4'
# cur=pymysql.cursors.DictCursor
# app.config['MYSQL_HOST']="https://mysql-26183-0.cloudclusters.net"
# app.config['MYSQL_PORT']=26183
# app.config['MYSQL_USER']= os.environ['MY_SQL_USERNAME']
# app.config['MYSQL_PASSWORD']= os.environ['MY_SQL_PASSWORD']
# app.config['MYSQL_DB']="perfect_trade_db"
# app.config['MYSQL_CURSORCLASS'] ="DictCursor"


# MysqlConnection().operate_database()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] =os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
mail = Mail(app)


from .routes import home
from .routes import users
from .routes import dashboard
from .routes import dashboard_api
from .routes import admin
