from perfect_trade import database,ma
import datetime
 
#messages model and schema
class messages(database.Model):
    __tablename__='messages'
    Id=database.Column('Id',database.Integer,primary_key=True)
    Lastname=database.Column(database.String(100))
    Firstname=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Message=database.Column(database.String(100))
    Subject=database.Column(database.String(100))
    Date_sent=database.Column(database.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self,message,firstname,lastname,email,subject):
        self.Lastname=lastname
        self.Firstname=firstname
        self.Subject=subject
        self.Email=email
        self.Message=message

class messageSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Lastname', 'Firstname','Email','Message','Date_sent')


#account model and schema
class account(database.Model):
    __tablename__='account'
    Id=database.Column('Id',database.Integer,primary_key=True)
    Name=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Currency=database.Column(database.String(100))
    Balance=database.Column(database.Integer)

    def __init__(self,name,email,currency,balance=0):
        self.Name=name
        self.Email=email
        self.Currency=currency
        self.Balance=balance
   

class accountSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Name', 'Email','Balance','Currency',)


#account_details model and schema
class account_details(database.Model):
    __tablename__='account_details'

    Id=database.Column('Id',database.Integer,primary_key=True)
    Name=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Account_Name=database.Column(database.String(100))
    Account_No=database.Column(database.Integer)
    Bank=database.Column(database.String(100))


    def __init__(self,name,email,acc_name,acc_no,bank):
        self.Name=name
        self.Email=email
        self.Account_Name=acc_name
        self.Account_No=acc_no
        self.Bank=bank

class acc_details_schema(ma.Schema):
    class Meta:
            fields = ('Id', 'Name', 'Email','Account_Name','Account_No')

#crypyo wallet models and schema
class wallet(database.Model):
    __tablename__='crypto_wallet'
    Id=database.Column('Id',database.Integer,primary_key=True)
    Wallet_ID=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Wallet_Type=database.Column(database.String(100))

    def __init__(self,wallet_id,email,wallet_type=0):
        self.Wallet_ID=wallet_id
        self.Email=email
        self.Wallet_Type=wallet_type
      
   

class walletSchema(ma.Schema):
    class Meta:
            fields = ('Wallet_ID', 'Email','Wallet_Type',)

#class users models and Schema
class Users(database.Model):
    __tablename__='perfect_trade_users'
    Id=database.Column('Id',database.Integer,primary_key=True)
    Lastname=database.Column(database.String(100))
    Firstname=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Password=database.Column(database.String(100))
    Customer_ID=database.Column(database.String(100))
    Date_Registered=database.Column(database.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self,firstname,lastname,email,password,cus_id):
        self.Lastname=lastname
        self.Firstname=firstname
        self.Customer_ID=cus_id
        self.Email=email
        self.Password=password

class userSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Lastname', 'Firstname','Email','Password','Date_Registered','Customer_ID')



# withdrawal schemas and Models
class withdrawals(database.Model):
    __tablename__='withrawals'

    Id=database.Column('Id',database.Integer,primary_key=True)
    Name=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Status=database.Column(database.String(100))
    Amount=database.Column(database.Integer)
    Currency=database.Column(database.String(100))
    Date=database.Column(database.DateTime(timezone=True), default=datetime.datetime.now())


    def __init__(self,name,email,acc_no,currency,date=datetime.datetime.now()):
        self.Name=name
        self.Email=email
        self.Status='Pending'
        self.Amount=acc_no
        self.Currency=currency
        self.Date=date

class withdrawSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Name', 'Email','Amount','Currency','Date')


#perfect Trade Adminidtrators Models and Schema
class Admin(database.Model):
    __tablename__='perfect_trade_adminstrators'

    Id=database.Column('Id',database.Integer,primary_key=True)
    Admin_Name=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Superuser=database.Column(database.String(100))
    Password=database.Column(database.String(100))
    Username=database.Column(database.String(100))
    Suspended=database.Column(database.String(100))


    def __init__(self,name,email,admin_name,password,superuser='False'):
        self.Admin_Name=admin_name
        self.Email=email
        self.Superuser=superuser
        self.Password=password
        self.Suspended='False'
        self.Date=date

class adminSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Admin_Name', 'Superuser','Password','Username','Suspended','Email')

# promo Model and Schema

class Promo(database.Model):
    __tablename__='promos'

    Id=database.Column('Id',database.Integer,primary_key=True)
    Promo_Name=database.Column(database.String(100))
    Date_to_End=database.Column(database.Date)
    Duration_in_Days=database.Column(database.Integer)
    Date_Started=database.Column(database.DateTime(timezone=True), default=datetime.datetime.now())
    Status=database.Column(database.String(100))
    Description=database.Column(database.String(100))
    Short_Description=database.Column(database.String(100))


    def __init__(self,name,end,des,short_desc,duration,status='Ongoing'):
        self.Promo_Name=name
        self.Status=status
        self.Date_Started=datetime.datetime.now()
        self.Date_to_End=end
        self.Description=desc
        self.Duration_in_Days=duration
        self.Short_Description=short_desc

class promoSchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Promo_Name', 'Date_Started','Date_to_End','Status','Description','Duration','Short_Description')

 
 #investment model and schema
class investments(database.Model):
    __tablename__='investments'

    Id=database.Column('Id',database.Integer,primary_key=True)
    Name=database.Column(database.String(100))
    Email=database.Column(database.String(100))
    Duration_Days=database.Column(database.Integer)
    Date_Invested=database.Column(database.DateTime(timezone=True), default=datetime.datetime.now())
    Amount=database.Column(database.Integer)
    Amount_Recieved=database.Column(database.Integer)
    Payment_Status=database.Column(database.String(100))
    Status=database.Column(database.String(100))
    Plan=database.Column(database.String(100))
    Percentage=database.Column(database.Integer)
    Currency=database.Column(database.Integer)
    Date_Of_Returns=database.Column(database.Date)


    def __init__(self,name,end,percent,currency,amt,amt_returned,email,plan,duration,status ='Ongoing',start=datetime.datetime.now()):
        self.Name=name
        self.Status=status
        self.Date_Invested=start
        self.Date_Of_Returns=end
        self.Amount=amt
        self.Amount_Recieved=amt_returned
        self.Duration_Days=duration
        self.Email=email
        self.Plan=plan
        self.Currency=currency
        self.Duration_in_Days=duration
        self.Percentage=percent

class investmentShchema(ma.Schema):
    class Meta:
            fields = ('Id', 'Name','Email','Date_Invested','Date_Of_Returns','Status','Description','Duration_Days','Amount','Amount_Recieved','Currency','Percentage','Payment_Status')






#user schema
new_user=userSchema()
new_users=userSchema(many=True,)

#message schema
new_message=messageSchema()
new_messages=messageSchema(many=True,)

#Promo Schema
new_promo=promoSchema()
new_promos=promoSchema(many=True,)

#admin schema
new_admin=adminSchema()
new_admins=adminSchema(many=True)

#User Schema
new_user=userSchema()
new_users=userSchema(many=True)

#wallet Schema
new_wallet=walletSchema()
new_wallets=walletSchema(many=True)

#investment Schema
new_investment=investmentShchema()
new_investments=investmentShchema(many=True)

#account Schema
new_account=accountSchema()
new_accounts=accountSchema(many=True)

#account details 
new_account_detail=acc_details_schema()
new_account_details=acc_details_schema(many=True)