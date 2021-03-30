from flask import Flask, render_template,redirect,logging,flash,url_for,session,request
from functools import wraps

def Authorize(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Please Login To  View Your Dashboard","red")
            return redirect(url_for("LogIn"))
    return wrap


def AuthorizeSignUp(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'details' in session and 'pin' in session:
            return f(*args,**kwargs)
        else:
            flash("Your Registeration Starts Here","red")
            return redirect(url_for("SignUp"))
    return wrap

def AuthorizePassChange(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'recovery' in session and 'recovery_pin' in session and 'recovery_email' in session :
            return f(*args,**kwargs)
        else:
            flash("Recovery Starts Here","red")
            return redirect(url_for("forgotPassword"))
    return wrap

def AuthorizeAdmin(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'admin' in session :
            return f(*args,**kwargs)
        else:
            flash("Unauthorized Access","red")
            return redirect(url_for("adminLogin"))
    return wrap