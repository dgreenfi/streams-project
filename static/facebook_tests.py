import requests
secret='43b0cd8cf372c106a81df203ff38c265'


url ='https://graph.facebook.com'
auth_endpoint='/oauth/access_token?client_id=847060522056698&client_secret='+secret+'&grant_type=client_credentials'
r=requests.get(url+auth_endpoint)
access_token=r.text

groups=[]
#find groups
purl='https://graph.facebook.com/search?q=cannabis&type=page&limit=100'
after=''
f=open('../data/facebookgroups.txt','w+')
for x in range(1,2):
    r=requests.get(purl+'&'+access_token+after)
    purl=r.json()['paging']['next']


    dat= r.json()['data']
    for page in dat[0:2]:
        pdata=requests.get('https://graph.facebook.com/v2.6/'+page['id']+'/likes?'+access_token)
        print pdata.json()
    groups.append(r.json()['data'])
#print groups
quit()

endpoint='/v2.4/8062627951/events'
endpoint='/v2.6/110103132351046/feed'
#print url+endpoint+'?'+access_token
r=requests.get(url+endpoint+'?'+access_token)
#print r.text