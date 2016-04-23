api_key='2e422f3070575576334c59683743332'

import requests
import json
import redis
import time
LOAD_BOARD=0

BASE_URL='https://api.meetup.com/'

groupids=open('../fullgroupdata.txt','r').readlines()
groupids=[g.replace("\n","") for g in groupids]
groupids=[json.loads(g) for g in groupids]

urlnames=[g['urlname'] for g in groupids]
#get meaningful boards posts>50
if LOAD_BOARD==1:
    boards=open('../data/boardsdata.txt','r').readlines()

else:
    f=open('../data/boardsdata.txt','w+')
    boards=[]
    for urln in urlnames[0:2]:
        r=requests.get(BASE_URL+urln+'/boards?key='+api_key)
        if 'errors' in r.json().keys():
            print 'throttled'
            time.sleep(60)
        for board in r.json():
            boards.append(board)
    f.write(json.dumps(boards))
    f.close()

#save to file

#get discussions on those boards

#get posts from discussions