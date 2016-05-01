import json
import pickle
groups=open('../fullgroupdata.txt','r+').readlines()
groups=[ json.loads(group) for group in groups]
topleaders={}
topgroups={}

for group in groups:
    print group
    if 'business' in group['description'].lower() or 'legal' in group['description'].lower():
        if ('polyamory' not in group['description'].lower() and 'psychedelic' not in group['description'].lower()):
            if group['state'] not in topgroups.keys():
                group['state']
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
