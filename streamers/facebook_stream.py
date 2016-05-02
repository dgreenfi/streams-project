import requests
secret='removed'


url ='https://graph.facebook.com'
auth_endpoint='/oauth/access_token?client_id=removed&client_secret='+secret+'&grant_type=client_credentials'
r=requests.get(url+auth_endpoint)
access_token=r.text
endpoint='/v2.4/8062627951/events'
endpoint='/v2.6/110103132351046/feed'
#print url+endpoint+'?'+access_token
r=requests.get(url+endpoint+'?'+access_token)
print r.text
