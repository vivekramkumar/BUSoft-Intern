from typing import final
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import sys 
import json

inp = json.loads(sys.argv[1])

data = pd.read_csv('E:\\intern\\threads1.csv')
incident= pd.read_csv('E:\\intern\\Incident.csv')
#data.rename(columns={'Incident Thread ID':'Thread ID'},inplace=True)
data.rename(columns={'Foreign Key':'Incident ID'},inplace=True)

#f3=data[["Incident ID","Text"]].merge(incident[["Incident ID","Status","Subject"]],on="Incident ID",how="left")
f3=data[["Incident Thread ID","Incident ID","Text","Thread Entry Type"]].merge(incident[["Incident ID","Status"]],on="Incident ID",how="left")
#header_row=0
#data.columns=data.iloc[header_row]
#print(data.head(2))

f3=f3[f3['Thread Entry Type']=='Customer']
f3=f3[f3['Status'] == 'Solved']
#data=f3["Subject"]
data=f3
data['Text']=data['Text'].str.replace("<div>",'')
data['Text']=data['Text'].str.replace("<div>",'')
data['Text']=data['Text'].str.replace('</div>','')
data['Text']=data['Text'].str.replace('\n','')
data['Text']=data['Text'].str.replace('<br>','')
data['Text']=data['Text'].str.replace('<br />','')
data['Text']=data['Text'].str.replace('<div style="margin:0px 0px 8px 0px;">','')
data['Text']=data['Text'].str.replace('<span>','')
data['Text']=data['Text'].str.replace('</span>','')
data=data[data['Text'].str.len()>12]

x=[]
for i in data['Text']:
    x.append(fuzz.token_sort_ratio(inp,i))
loc=x.index(max(x))
#data['Text'].iloc[loc]
y=sorted(range(len(x)), key=lambda i: x[i], reverse=True)[:5]
finaldata=[]

class record:
    def __init__(self, incidentid, text,threadid):
        self.incidentid = incidentid
        self.text = text
        self.threadid=threadid
#print('[')
for i,j in enumerate(y):
    finaldata.append(record(data['Incident ID'].iloc[j],data['Text'].iloc[j],data['Incident Thread ID'].iloc[j]))
    #print([data['Incident ID'].iloc[j],data['Text'].iloc[j],data['Incident Thread ID'].iloc[j]])
    print(finaldata[i].__dict__)
    #print((finaldata[i]))
#print(json.dumps(finaldata,default=record.__dict__))
#print(']')
sys.stdout.flush()
    #finaldata.append(i+1)
    #finaldata.append(data['Text'].iloc[j])
    #finaldata.append(Incident Thread ID.iloc[j])
#print(json.dumps(finaldata))
