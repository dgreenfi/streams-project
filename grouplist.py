
api_key='2e422f3070575576334c59683743332'

import requests
import json
from bs4 import BeautifulSoup
BASE_URL='https://api.meetup.com'
GROUPS_EP='/find/groups'
EVENTS_EP='/self/events'
#search term list
TERMS=['marijuana','Cannabis','420','Ganja','Marijuna']
#election state list for limiting
ELECTION_STATES=['OH','MI','AZ','AR','CA','ME','MA','MO','MT','NV','ND','OK']



ids=[]
groups=[]
egroups=[]
req_params='key='+api_key+'&'+'sign=true'
rj=['temp']
i=0
#page through responses to get max responses for each request
for term in TERMS:
    while len(rj)>0:
        r=requests.get(BASE_URL+GROUPS_EP+'?'+'text='+term+'&'+req_params+'&radius=global&page=200&offset='+str(i))
        rj=r.json()
        print len(rj)
        for group in rj:
            if group['id'] not in ids:
                ids.append(group['id'])
                groups.append(json.dumps(group))
                #create election group sublist
                if group['state'] in ELECTION_STATES:
                   egroups.append(group)
        i+=1
    rj=['temp']
    i=0
print len(egroups),len(groups)
egroups = sorted(egroups, key=lambda k: k['members'])
egroups = [json.dumps(k) for k in egroups]
f= open('groupids.txt','w+')
f2= open('fullgroupdata.txt','w+')
f3= open('electionstategroups.txt','w+')
for id in ids:
    f.write(str(id)+'\n')

for group in groups:
    f2.write(group +'\n')

for group in egroups:
    f3.write(group +'\n')


