import redis
from collections import Counter
import urllib2
import time
import json
from urllib2 import urlopen
from lxml.html import parse

REDIS_PORT=9999
conn_top=redis.Redis(port=REDIS_PORT,db=4)
conn_top_title=redis.Redis(port=REDIS_PORT,db=5)
conn_hashtag=redis.Redis(db=2,port=REDIS_PORT)
conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)
conn_counts=redis.Redis(db=7,port=REDIS_PORT)
#counts db will store type + array like "urls":[21,19,12,3,2,1]

def main():
    while True:
        #calculate top hashtags
        hashtags_calc()
        #calculate top urls
        urls=get_links()
        #crawl and parse top URL's for displayable title
        titles_from_urls(urls)
        #calculate twitter colume
        twitter_volume()
        #wait 60 seconds and repeat
        time.sleep(60)


def twitter_volume():
    #stores a time series of volumes
    conn=redis.Redis(db=0,port=REDIS_PORT)
    keys=conn.keys()
    #add to list on left
    conn_counts.lpush('volume',len(keys))
    return

def get_links():
    #grab raw URL data
    conn_link=redis.Redis(port=REDIS_PORT,db=1)
    keys=conn_link.keys()
    values = conn_link.mget(keys)
    counts=Counter(values)
    n=min(10,len(counts))
    #calculate most common 10
    urls=counts.most_common(n)
    turls=[u[0] for u in urls]
    curls=[u[1] for u in urls]
    #clean up formatting issue with quotes
    for i,x in enumerate(turls):
        conn_top.set(i,x.replace('"',""))
    conn_counts.set('urls',json.dumps(curls))
    return turls

def titles_from_urls(urls):
    #takes input of urls
    titles=[]
    #method to make webcall and fetch HTML
    for i,url in enumerate(urls):
        url=url.replace('"',"")
        try:
            #make get request and parse HTML to find title field
            page = urlopen(url)
            p= parse(page)
            title=p.find(".//title").text
        #tried a specific HTTP error but didn't cover all options.  broad error actually make sense in this case given broad response
        except:
            #if anything fails retur that the title is not available
            title='Title Not Available'
        titles.append(title )
        #set corresponding list of titles
        conn_top_title.set(i,title.replace('\n',"").encode('ascii','ignore'))
    return titles

def hashtags_calc():
    #grab raw hashtag records
    keys=conn_hashtag.keys()
    values = conn_hashtag.mget(keys)
    counts=Counter(values)
    n=min(10,len(counts))
    #find top 10
    counts=counts.most_common(n)
    count_array=[]
    hashtag_array=[n[0] for n in counts]
    for i,x in enumerate(counts):
        count_array.append(x[1])
    conn_hashtag_counts.set('hashtags',json.dumps(hashtag_array))
    #write array of top 10 to redis db
    conn_counts.set('hashtags',json.dumps(count_array))
    return counts

if __name__!='main':

    main()