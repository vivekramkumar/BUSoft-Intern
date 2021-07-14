import pandas as pd
import warnings
import csv
import json
import sys
from rank_bm25 import BM25Okapi

from timeit import default_timer as timer
from cleaned import clean
warnings.filterwarnings("ignore")
inp = json.loads(sys.argv[1])
#inp=input()
#t0 = timer()
df = pd.read_csv('E:\\intern\\threads1.csv')
incident= pd.read_csv('E:\\intern\\Incident.csv')
df=clean(df,incident)

final=[]
with open('E:\\intern\\final_full_length.csv', newline='',encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    final.append(data)

bm25 = BM25Okapi(data)

query = inp
tokenized_query = query.lower().split(" ")

results = bm25.get_top_n(tokenized_query, df.Text.iloc[:len(data)].values, n=5)

finaldata={"incident_id":1,"text":"test","thread_id":1}
finaljson=[]
for i in results:
    inc_id=int(df['Incident ID'][df['Text']==i])
    text=i
    thread_id=int(df['Incident Thread ID'][df['Text']==i])
    finaldata["incident_id"]=inc_id
    finaldata["text"]=text
    finaldata['thread_id']=thread_id
    finaljson.append(finaldata.copy())
#t1 = timer()
jsonstr = json.dumps(finaljson)
#print("Time elapsed = ",t1-t0,"seconds")

print(jsonstr)
#sys.stdout.flush()