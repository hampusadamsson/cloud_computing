from celery import Celery
import json
from collections import Counter

app = Celery('tasks', backend='rpc://', broker='amqp://')




@app.task
def getJson():
    with open("/home/hampus/skola/CloudComputing/FilesFromAssignments2015-09-15/C3/localSolution/tweets.txt") as f:
        content = f.readlines()
    tmp = runme.delay(content)
    return tmp

@app.task
def runme(Jdata):
    tmp = Counter()

    for item in Jdata:
        if(1<len(item)): # Removes Empty rows
            tmp = tmp + manageRow.delay(item)            
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

import os
from sys import argv
import time
from novaclient.client import Client
import uuid
import swiftclient.client

config = {'username':os.environ['OS_USERNAME'],
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

nc = Client('2',**config)

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

a = conn.get_object("tweets", 'tweets_0.txt')
