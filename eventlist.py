
api_key='2e422f3070575576334c59683743332'

import requests
import json
from bs4 import BeautifulSoup
BASE_URL='https://api.meetup.com'
GROUPS_EP='/find/groups'
EVENTS_EP='/2/events'
req_params='key='+api_key+'&'+'sign=true'


f = open('groupids.txt','r+')
f2= open('fullgroupdata.txt','r+')

ids=f.readlines()
ids=[id.replace('\n','') for id in ids]

count=0
for id in ids:
    e=requests.get(BASE_URL+EVENTS_EP+'?'+'group_id='+id+'&'+req_params)
    print e.text
    if len(e.json()['results'])>0:
        count+=1

    #print len(e.json())
print count



