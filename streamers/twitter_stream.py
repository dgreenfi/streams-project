import tweepy
import redis
import json


REDIS_PORT=9999


conn=redis.Redis(db=0,port=REDIS_PORT)
conn_url=redis.Redis(db=1,port=REDIS_PORT)
conn_hashtag=redis.Redis(db=2,port=REDIS_PORT)

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        try:
            text=decoded['text'].encode('ascii', 'ignore')
        except KeyError:
            print decoded
            return
        checkwords=['legal',' vote ',' law ','business','revenue','sales']
        check=sum([(word in text.lower()) for word in checkwords])

        if len(text)>30:
            if check>1:
                # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
                conn.setex(decoded['id'],json.dumps(decoded),9600)
                for url in decoded['entities']['urls']:
                    conn_url.setex(decoded['id'],json.dumps(url['expanded_url']),9600)
                for tag in decoded['entities']['hashtags']:
                    if tag['text'].lower() not in ['cannabis','marijuana','weed']:
                        conn_hashtag.setex(decoded['id'],json.dumps(tag['text'].lower()),9600)
                        print "Archived"
                return True

    def on_error(self, status):
        print status

def load_creds(credloc):
    #load keys from key file
    with open(credloc) as data_file:
        data = json.load(data_file)
    return data

if __name__ == '__main__':
    l = StdOutListener()
    creds=load_creds('../cred/keys.txt')
    auth = tweepy.OAuthHandler(creds['twitter_key'], creds['twitter_secret'])
    auth.set_access_token(creds['twitter_access_token'], creds['twitter_token_secret'])



    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=['cannabis','marijuana'])