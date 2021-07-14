import re
from nltk.stem import WordNetLemmatizer
wordLemm = WordNetLemmatizer()

def clean(df,incident):
    df.rename(columns={'Foreign Key':'Incident ID'},inplace=True)

    #f3=data[["Incident ID","Text"]].merge(incident[["Incident ID","Status","Subject"]],on="Incident ID",how="left")
    f3=df[["Incident Thread ID","Incident ID","Text","Thread Entry Type"]].merge(incident[["Incident ID","Status"]],on="Incident ID",how="left")
    #header_row=0
    #data.columns=data.iloc[header_row]
    #print(data.head(2))
    f3.set_index('Incident Thread ID')
    f3=f3[f3['Thread Entry Type']=='Customer']
    f3=f3[f3['Status'] == 'Solved']
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
    df['Text']=df['Text'].str.replace('==================== text File Attachment ====================','')
    #df['Text']=df['Text'].str.replace('+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------','')
    df=df[df['Text'].str.len()>12]
    return df

def preprocess_text(data):
    preprocessed=[]
    for text in data:
        text=str(text)
        text=re.sub(r'@[A-Za-z0-9]+'," ",text) 
        text=re.sub(r'^[A-Za-z0-9.!?]+'," ",text) 
        text=re.sub(r'https?://[A-Za-z0-9./]+'," ",text) 
        text=re.sub(r' +'," ",text)
        text = text.lower()
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"\'scuse", " excuse ", text)
        text = text.strip(' ')
        text = text.strip('. .')
        text = text.replace('.',' ')
        text = text.replace('-',' ')
        text = text.replace("’", "'").replace("′", "'").replace("%", " percent ").replace("₹", " rupee ").replace("$", " dollar ")
        text = text.replace("won't", "will not").replace("cannot", "can not").replace("can't", "can not")
        text = text.replace("€", " euro ").replace("'ll", " will")
        text = text.replace("don't", "do not").replace("didn't", "did not").replace("im","i am").replace("it's", "it is")
        text = text.replace(",000,000", "m").replace("n't", " not").replace("what's", "what is")
        text = text.replace(",000", "k").replace("'ve", " have").replace("i'm", "i am").replace("'re", "are")
        text = text.replace("he's", "he is").replace("she's", "she is").replace("'s", " own")
        text = re.sub('\s+', ' ', text)

        textwords = ''
        for word in text.split():
            if len(word)>1:
                word = wordLemm.lemmatize(word)
                textwords += (word+' ')
        preprocessed.append(textwords)
    return preprocessed