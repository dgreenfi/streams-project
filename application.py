from flask import Flask
from flask import render_template
from meetup_func import group_dates
from flask import request, send_from_directory

application = Flask(__name__)
import json

@application.route('/')
def display():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='growth.html')

@application.route('/legis')
def legis():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='legislation.html')

@application.route('/projection')
def projection():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='projection.html')

@application.route('/community')
def community():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='community.html')

@application.route('/bio')
def info():
    temp=request.args.get('template')
    return render_template(temp)

if __name__ == '__main__':
    application.run(debug=True)