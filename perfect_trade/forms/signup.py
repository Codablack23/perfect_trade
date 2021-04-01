from wtforms import Form,StringField,PasswordField,TextAreaField,validators
import re
from passlib.hash import sha256_crypt

class SignUpForm(Form):
  surname=StringField('', [
     validators.Length(min=3,max=50,message="Surname is Too Short"),
     validators.DataRequired()
   ])
  firstName=StringField('', [
     validators.Length(min=3,max=50,message="Username is Too Short"), validators.DataRequired()
   ])
  email=StringField('',[validators.Length(min=5,max=50,message="Invalid Email Length"), validators.DataRequired()])
  password=PasswordField("",[
     validators.Length(min=8,max=50, message="Password Must atleast Be 8 Characters Long"),
     validators.DataRequired()
  ])
  confirm_password = PasswordField('',[
     validators.DataRequired(),
     validators.EqualTo('password', message="Passwords Do not Match")
  ])

