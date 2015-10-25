from celery import Celery
import json
from collections import Counter
import os
from sys import argv
import time
import uuid
import swiftclient.client
    

app = Celery('tasks', backend='rpc://', broker='amqp://')

@app.task
def runme(Jdata):
    tmp = Counter()

    for item in Jdata:
        if(1<len(item)): # Removes Empty rows
            tmp = tmp + manageRow(item)            
    return(tmp)

@app.task
def manageRow(item):
    result = Counter()
    data = json.loads(item)
    if('retweeted_status' not in data.keys()): #Removes retweets
        result  = Counter(data['text'].split())
    return result

#
# 
#


@app.task
def go():
    config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

    conn = swiftclient.client.Connection(auth_version=2, **config)

    return(conn.get_object("tweets", 'tweets_0.txt'))
    
