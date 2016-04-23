import redis
from collections import Counter
import urllib2
import time
REDIS_PORT=9999
conn_top=redis.Redis(port=REDIS_PORT,db=4)
conn_top_title=redis.Redis(port=REDIS_PORT,db=5)
conn_hashtag=redis.Redis(db=2,port=REDIS_PORT)
conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)

def main():
    while True:
        hashtags_calc()
        urls=get_links()
        titles_from_urls(urls)
        time.sleep(120)



def get_links():
    conn_link=redis.Redis(port=REDIS_PORT,db=1)
    keys=conn_link.keys()
    values = conn_link.mget(keys)
    counts=Counter(values)
    n=min(10,len(counts))
    urls=counts.most_common(n)
    urls=[u[0]for u in urls]
    for i,x in enumerate(urls):
        conn_top.set(i,x.replace('"',""))
    return urls

def titles_from_urls(urls):

    titles=[]
    for i,url in enumerate(urls):
        url=url.replace('"',"")
        from urllib2 import urlopen
        from lxml.html import parse
        try:
            page = urlopen(url)
            p= parse(page)
            title=p.find(".//title").text
        #tried a specific HTTP error but didn't cover all options.  broad error actually make sense in this case given broad response
        except:
            title='Title Not Available'
        titles.append(title )
        conn_top_title.set(i,title.replace('\n',"").encode('ascii','ignore'))
    return titles

def hashtags_calc():
    keys=conn_hashtag.keys()
    values = conn_hashtag.mget(keys)
    counts=Counter(values)
    n=min(10,len(counts))
    counts=counts.most_common(n)
    for i,x in enumerate(counts):
        conn_hashtag_counts.set(i,x[0].replace('"',""))
    return counts

if __name__!='main':

    conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)
    keys=conn_hashtag_counts.keys()
    print keys
    #values = conn_hashtag_counts.mget(keys)
    #print values
    main()