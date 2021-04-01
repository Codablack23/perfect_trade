from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail

app = Flask(__name__)
secret_key="qwertyuiopasdfghjkl11"
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= ""
app.config['MYSQL_DB']="perfect_trade_db"
app.config['MYSQL_CURSORCLASS'] ="DictCursor"
mysql=MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "goodluckedih@gmail.com"
app.config['MAIL_PASSWORD'] = "goodybag23"
mail = Mail(app)


from .routes import home
from .routes import user
from .routes import dashboard
from .routes import dashboard_api
from .routes import admin