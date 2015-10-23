from celery import Celery
import json
from collections import Counter

#app = Celery('tasks', broker='amqp://guest@localhost//')
app = Celery('tasks', backend='rpc://', broker='amqp://')
#app = Celery('tasks', backend='redis://localhost', broker='amqp://')

@app.task
def getJson():
    with open("/home/hampus/skola/CloudComputing/FilesFromAssignments2015-09-15/C3/localSolution/tweets.txt") as f:
        content = f.readlines()
    tmp = runme.delay(content)
    return tmp


# INPUT = list 
# Varje rad motsvarar en array. varannat.
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

#runme(getJson())
