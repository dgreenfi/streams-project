import json
import pickle
groups=open('../fullgroupdata.txt','r+').readlines()
groups=[ json.loads(group) for group in groups]
topleaders={}
topgroups={}

for group in groups:

    if group['state'] not in topgroups.keys():
        topgroups[group['state']]=group
    else:
        print group['state'],group['members'],topgroups[group['state']]['members']
        if group['members']>topgroups[group['state']]['members']:
            topgroups[group['state']]=group

for key in topgroups.keys():
    topleaders[key]=topgroups[key]['organizer']

pickle.dump(topgroups,open('../data/topgroups.txt','w+'))
pickle.dump(topgroups,open('../data/topleaders.txt','w+'))


#print topleaders
