from celery import Celery
import json
from collections import Counter
import os
from sys import argv
import time
import uuid
import swiftclient.client    
import StringIO
import os

app = Celery('tasks', backend='rpc://', broker='amqp://')

# @app.task
# def runme(Jdata):
#     tmp = Counter()

#     for item in Jdata:
#         if(1<len(item)): # Removes Empty rows
#             tmp = tmp + manageRow(item)            
#     return(tmp)

@app.task
def manageRow(item):
    prons = Counter()
    result = Counter()
    data = json.loads(item)
    if('retweeted_status' not in data.keys()): #Removes retweets
        result  = Counter(data['text'].split())
        
        prons = Counter({'han':result['han'],'hon':result['hon'],'den':result['det'],'denna':result['denna'],'denne':result['denne'],'hen':result['hen']})
        
    return prons

#
# 
#
@app.task
def splitit(data):
    result = Counter()
    ans = "start"
    buf = StringIO.StringIO(data)

    while(len(ans)>0):
        ans = buf.readline()
        if(len(ans)>1):
            result = result + manageRow(ans)
    return result

@app.task
def go():
    import os
    from sys import argv
    import time
    from novaclient.client import Client
    import uuid
    import swiftclient.client
    result = Counter()

    config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
    
    conn = swiftclient.client.Connection(auth_version=2, **config)

    container_name = "adams"
    tmp = conn.get_container(container_name)
    for num in range(0,len(tmp[1])):
        item = tmp[1][num]['name']
        data = conn.get_object(container_name, item)
        result = result + splitit(data[1])
    return(result)
    
a = go.delay()
b = a.get()
print(b)
