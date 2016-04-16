import json
import datetime


def group_dates():
    today = datetime.date.today()

    by_month=[]
    groups=[]
    f=open('./fullgroupdata.txt')

    data=f.readlines()
    data=[json.loads(line) for line in data]


    for x in data:
        groups.append((datetime.datetime.fromtimestamp(x['created']/1000).strftime('%Y'),x['name'],x['lat'],x['lon']))

    groups = sorted(groups, key=lambda tup: tup[0])
    yeardict={}
    for g in groups:
        try:
            yeardict[g[0]].append((g[1],g[2],g[3]))
        except KeyError:
            yeardict[g[0]]=[]
            yeardict[g[0]].append((g[1],g[2],g[3]))
    years=[key for key in yeardict.keys()]
    years.sort()
    groups=[]
    for key in years:
        groups.append(yeardict[key])
        print len(yeardict[key])
    #print years
    return years,groups

if __name__!='main':
    group_dates()
