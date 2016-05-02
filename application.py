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
    wash_sales = get_wash_sales()
    wash_stores = get_wash_stores()
    col_sales = get_col_sales()
    return render_template('coretemp.html',
        sales=wash_sales,sales2=col_sales,stores=wash_stores,page='growth.html')

@application.route('/legis')
def legis():
    return render_template('coretemp.html',page='legislation.html',side='sidemap.html')

@application.route('/projection')
def projection():
    california_sales = get_state_projections('California')
    nevada_sales = get_state_projections('Nevada')
    vermont_sales = get_state_projections('Vermont')
    arizona_sales = get_state_projections('Arizona')
    conn_sales = get_state_projections('Connecticut')
    mich_sales = get_state_projections('Michigan')
    ri_sales = get_state_projections('Rhode Island')
    total_likely = get_all_projections('data/total-likely.csv')
    maybe_likely = get_all_projections('data/maybe-total.csv')
    lyr_sales,lyr_sales_num=yearly_sales(total_likely)
    myr_sales,myr_sales_num=yearly_sales(maybe_likely)
    tsales=[to_millions(x+y) for x, y in zip(lyr_sales_num, myr_sales_num)]
    print tsales
    return render_template('coretemp.html', sales=california_sales, sales2=nevada_sales, 
        sales3=vermont_sales, sales4=arizona_sales, sales5=conn_sales, sales6=mich_sales, 
        sales7=ri_sales, sales8=total_likely, sales9=maybe_likely,lyr_sales=lyr_sales,myr_sales=myr_sales,tsales=tsales, page='projection.html')


def to_millions(num):
    n=int(num/1000000)
    n=str(n)
    n_new=''
    for c in reversed(n):
        if len(n_new)>0:
            if len(n_new)%3==0:
                n_new = ','+n_new
        n_new=c+n_new

    return n_new + " million"

def yearly_sales(series):
    #convert to annual sales figs
    r_total=0
    r_added=[]
    yr_sales=[]
    yr_sales_num=[]
    for x in series:
        r_added.append(x)
        r_total+=x[1]
        if len(r_added)==12:
            yr_sales.append(to_millions(r_total))
            yr_sales_num.append(r_total)
            r_total=0
            r_added=[]
    return yr_sales,yr_sales_num


@application.route('/community_growth')
def community_growth():
    f=open('groupids.txt')
    ids=f.readlines()
    ids=[i.replace('\n','') for i in ids]
    y,g= group_dates()
    return render_template('coretemp.html',events=json.dumps(ids),years=y,groups=g,page='community_growth.html')


@application.route('/community')
def community():
    states=['AZ','AK','MA','MI','MO','NV','OH','CA','MA']
    meetups=get_top_groups()
    leaders=get_group_leads()
    return render_template('coretemp.html',page='community.html',
                           states=states,meetups=meetups,leaders=leaders)


@application.route('/communityconv')
def community_conv():
    urls=get_links()
    titles=get_titles()
    links=zip(urls,titles)
    hashtags=get_hashtags()
    hcounts=get_hashtag_counts()
    ucounts=get_url_counts()
    tvol=get_twitter_vol()
    return render_template('coretemp.html',page='community_conv.html',links=links,
                           hashtags=hashtags,hcounts=hcounts,ucounts=ucounts,tvol=tvol)


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

def get_twitter_vol():
    conn_twitter_num=redis.Redis(db=7,port=REDIS_PORT)
    last10=conn_twitter_num.lrange('volume',0,360)
    last10.reverse()
    time=range(0, len(last10))
    chartdata=[]
    for x in range(0,len(last10)):
        chartdata.append([time[x],int(last10[x])])
    return chartdata

def get_wash_sales():
    sales = []
    f = open('data/wash-sales.csv')
    f.readline()
    for l in f:
        split = l.split(',')
        year,month,sale = int(split[0]), int(split[1]), int(split[2])
        sales.append([year, month, sale])
    return sales

def get_col_sales():
    sales = []
    f = open('data/coloradoretail.csv')
    f.readline()
    for l in f:
        split = l.split(',')
        month,year,sale = int(split[0]), int(split[1]), int(split[2]) / 0.1
        sales.append([year, month, sale])

    return sales

def get_wash_stores():
    stores = []
    f = open('data/wash-stores.csv')
    f.readline()
    for l in f:
        split = l.split(',')
        year,month,store = int(split[0]), int(split[1]), int(split[2])
        stores.append([year, month, store])

    return stores

def get_state_projections(state):
    chartdata = []
    f = open('data/projectedrevenues.csv')
    for l in f:
        split = l.split(',')
        if split[0] != state:
            continue
        month, revenue = int(split[1]), float(split[2])
        chartdata.append([month, revenue])
    return chartdata

def get_all_projections(f_name):
    chartdata = []
    f = open(f_name)
    for l in f:
        split = l.split(',')
        month, revenue = int(split[0]), float(split[1])
        chartdata.append([month, revenue])
    return chartdata

def get_hashtags():
    conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)
    values = conn_hashtag_counts.get('hashtags')
    array=json.loads(values)
    array=[x.replace('"',"") for x in array]
    return array

def get_hashtag_counts():
    conn_hashtag_num=redis.Redis(db=7,port=REDIS_PORT)
    values = conn_hashtag_num.get('hashtags')
    array=json.loads(values)
    array=[x for x in array]
    return array

def get_url_counts():
    conn_hashtag_num=redis.Redis(db=7,port=REDIS_PORT)
    values = conn_hashtag_num.get('urls')
    print values
    array=json.loads(values)
    array=[x for x in array]
    return array

def get_top_groups():
    groups=pickle.load(open('./data/topgroups.txt','r+'))
    return groups

def get_group_leads():
    leads=pickle.load(open('./data/topleaders.txt','r+'))
    return leads

if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0')