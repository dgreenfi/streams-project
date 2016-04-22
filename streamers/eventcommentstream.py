from websocket import create_connection
import json

ws = create_connection("ws://stream.meetup.com/2/event_comments")

print "Receiving..."
while True:
    result = ws.recv()
    rjson=json.loads(result)
    print rjson
