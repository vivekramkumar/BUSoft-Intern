import pandas as pd
import warnings
import csv
import spacy
from tqdm import tqdm

warnings.filterwarnings("ignore")
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



nlp = spacy.load("en_core_web_sm")
tok_text=[] # for our tokenised corpus
#Tokenising using SpaCy:
for doc in tqdm(nlp.pipe(df.Text.iloc[:].str.lower().values, disable=["tagger", "parser","ner","lemmatizer"])):
    tok = [t.text for t in doc if t.is_alpha]
    tok_text.append(tok)
with open("E:\\intern\\final_full_length.csv", "w", newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(tok_text)
