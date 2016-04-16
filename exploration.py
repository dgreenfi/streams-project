
api_key='2e422f3070575576334c59683743332'

import requests
from bs4 import BeautifulSoup
BASE_URL='https://api.meetup.com'
GROUPS_EP='/find/groups'
EVENTS_EP='/self/events'

def strip_html(blob):
    soup = BeautifulSoup(blob)
    text = soup.getText()
    return text

def main():
    req_params='key='+api_key+'&'+'sign=true'
    r=requests.get(BASE_URL+GROUPS_EP+'?'+'text=cannabis'+'&'+req_params)
    rj=r.json()
    print len(rj)

    f = open("testing.txt",'w')
    for meetup in rj:
        f.write(':::'+meetup['name']+':::\n')
        f.write('Members:'+str(meetup['members'])+'\n')
        f.write(strip_html(meetup['description']).encode('utf-8')+'\n\n\n')
    #save_to_file(r.text,"testing.txt")
    print (r.text)

    #fetch event
    urlname='/cansociety/events/'
    print BASE_URL+urlname+'228314912'+'?'+req_params
    r=requests.get(BASE_URL+urlname+'228314912'+'?'+req_params)
    print r.text




if __name__ == '__main__':
    main()