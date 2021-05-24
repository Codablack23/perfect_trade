from flask import Flask, render_template,redirect,logging,flash,url_for,session,request,jsonify
from perfect_trade import app


@app.route('/training')
def Training():
    title="Training Registration Has Not Started"
    body="Our Training Registeration Has Not Commenced Yet But In due time We Will Update Our Site When Registeration Have Started And Inform You when We Start"
    return render_template("Trainings/training.html", Page="Training", alert_title=title,alert_body=body)

@app.route('/signals')
def Signals():
    title="Subscription Has Not Started"
    body="Currently We Have Not Started Subscription TO Our Signals But We Will Inform You when Our Subscription Has Started"
    return render_template("Trainings/signals.html", Page="Signals",alert_title=title,alert_body=body)

