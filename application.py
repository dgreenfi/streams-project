from flask import Flask
from flask import render_template
from pyfunctions.meetup_func import group_dates
application = Flask(__name__)
import json

@application.route('/')
def display():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('livedisplay.html',events=json.dumps(ids),years=y,groups=g)

if __name__ == '__main__':
    application.run(debug=True)