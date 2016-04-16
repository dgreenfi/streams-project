
api_key='2e422f3070575576334c59683743332'

import requests
import json
from bs4 import BeautifulSoup
BASE_URL='https://api.meetup.com'
GROUPS_EP='/find/groups'
EVENTS_EP='/self/events'

TERMS=['marijuana','Cannabis','420','Ganja','Marijuna']
ids=[]
groups=[]
req_params='key='+api_key+'&'+'sign=true'
rj=['temp']
i=0
for term in TERMS:
    while len(rj)>0:
        r=requests.get(BASE_URL+GROUPS_EP+'?'+'text='+term+'&'+req_params+'&radius=global&page=200&offset='+str(i))
        rj=r.json()
        print len(rj)
        for group in rj:
            ids.append(group['id'])
            groups.append(json.dumps(group))
        i+=1
    rj=['temp']
    i=0

f = open('groupids.txt','w+')
f2= open('fullgroupdata.txt','w+')
for id in ids:
    f.write(str(id)+'\n')

for group in groups:
    f2.write(group +'\n')


