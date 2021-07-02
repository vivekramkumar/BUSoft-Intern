import pandas as pd
import warnings
import csv
import json
import sys

warnings.filterwarnings("ignore")
inp = json.loads(sys.argv[1])
#print("test")
#inp=input()

df = pd.read_csv('E:\\intern\\threads1.csv')
incident= pd.read_csv('E:\\intern\\Incident.csv')
#data.rename(columns={'Incident Thread ID':'Thread ID'},inplace=True)
df.rename(columns={'Foreign Key':'Incident ID'},inplace=True)

#f3=data[["Incident ID","Text"]].merge(incident[["Incident ID","Status","Subject"]],on="Incident ID",how="left")
f3=df[["Incident Thread ID","Incident ID","Text","Thread Entry Type"]].merge(incident[["Incident ID","Status"]],on="Incident ID",how="left")
#header_row=0
#data.columns=data.iloc[header_row]
#print(data.head(2))
f3.set_index('Incident Thread ID')
f3=f3[f3['Thread Entry Type']=='Customer']
f3=f3[f3['Status'] == 'Solved']
#data=f3["Subject"]
df=f3
df['Text']=df['Text'].str.replace("<div>",'')
df['Text']=df['Text'].str.replace("<div>",'')
df['Text']=df['Text'].str.replace('</div>','')
df['Text']=df['Text'].str.replace('\n','')
df['Text']=df['Text'].str.replace('<br>','')
df['Text']=df['Text'].str.replace('<br />','')
df['Text']=df['Text'].str.replace('<div style="margin:0px 0px 8px 0px;">','')
df['Text']=df['Text'].str.replace('<span>','')
df['Text']=df['Text'].str.replace('</span>','')
df=df[df['Text'].str.len()>12]

final=[]
with open('E:\\intern\\final_full_length.csv', newline='',encoding="utf-8") as f:
    reader = csv.reader(f)
    data = list(reader)
    final.append(data)

from rank_bm25 import BM25Okapi
bm25 = BM25Okapi(data)

query = inp
tokenized_query = query.lower().split(" ")
import time

t0 = time.time()
results = bm25.get_top_n(tokenized_query, df.Text.iloc[:len(data)].values, n=5)
t1 = time.time()
print(f'Searched {len(data)} records in {round(t1-t0,3) } seconds \n')

class record:
    def __init__(self, incidentid, text,threadid):
        self.incident_id = incidentid
        self.text = text
        self.thread_id=threadid

finaldata=[]
for i in results:
    inc_id=int(df['Incident ID'][df['Text']==i])
    text=i
    thread_id=int(df['Incident Thread ID'][df['Text']==i])
    finaldata.append(record(inc_id,i,thread_id))
    
for i in range(len(results)):
    print(finaldata[i].__dict__,',')
    sys.stdout.flush()
