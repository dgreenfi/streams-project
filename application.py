from flask import Flask
from flask import render_template
from meetup_func import group_dates
from flask import request, send_from_directory
import pickle
import redis
application = Flask(__name__)
import json
import lxml.html
from collections import Counter

REDIS_PORT=9999

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
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='legislation.html',side='sidemap.html')

@application.route('/projection')
def projection():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='projection.html')

@application.route('/community')
def community():

    states=['AZ','AK','MA','MI','MO','NV','OH','CA','MA']
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    meetups=get_top_groups()
    leaders=get_group_leads()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='community.html',
                           states=states,meetups=meetups,leaders=leaders)


@application.route('/communityconv')
def community_conv():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    urls=get_links()
    titles=get_titles()
    links=zip(urls,titles)
    hashtags=get_hashtags()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='community_conv.html',links=links,
                           hashtags=hashtags)


@application.route('/bio')
def info():
    temp=request.args.get('template')
    return render_template(temp)


def get_links():
    conn_link=redis.Redis(port=REDIS_PORT,db=4)
    keys=conn_link.keys()
    values = conn_link.mget(keys)

    return values

def get_titles():
    conn_link=redis.Redis(port=REDIS_PORT,db=5)
    keys=conn_link.keys()
    values = conn_link.mget(keys)

    return values

def get_hashtags():
    conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)
    keys=conn_hashtag_counts.keys()
    values = conn_hashtag_counts.mget(keys)
    return values

def get_top_groups():
    groups=pickle.load(open('./data/topgroups.txt','r+'))
    return groups

def get_group_leads():
    leads=pickle.load(open('./data/topleaders.txt','r+'))
    return leads

if __name__ == '__main__':
    application.run(debug=True)