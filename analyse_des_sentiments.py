import csv
import pandas as pd
import re

import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import plotly.express as px

#Fonction de suppression des éléments non utiles 
def remove_content(text):
    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    text = re.sub(r"https\S+", " ", text) #remove urls
    text = text.replace('t.co', ' ')
    text = text.replace('&amp', ' ')
    text = re.sub(r"http\S+", "", text) #remove urls
    text=re.sub(r'\S+\.com\S+','',text) #remove urls
    text=re.sub(r'\@\w+','',text) #remove mentions
    text =re.sub(r'\#\w+','',text) #remove hashtags
    return text

#Lecture du csv
#A MODIFIER
df = pd.read_csv('fichiers/all_tweets_realDonaldTrump_cleaned.csv')

#creation d'un autre champs sans steminisation
df['tweet_sans_residu']=df['tweet'].apply(lambda x: remove_content(x)) 

#Détection des sentiments à partir du champ crée
#cet indicateur est noté entre -1 et 1, -1 étant un sentiment négatif et 1 un sentiment positif
df['sentiment']=df['tweet_sans_residu'].apply(lambda x:TextBlob(x).sentiment[0])
#Détection des tweets subjectifs 
#cet indicateur est noté entre 0 et 1. Plus la valeur est proche de 1, plus le texte peut être considéré comme subjectif
df['subject']=df['tweet_sans_residu'].apply(lambda x: TextBlob(x).sentiment[1])
#polarité positive ou négative selon le sentiment
df['polarity']=df['sentiment'].apply(lambda x: 'pos' if x>=0 else 'neg')
#sauvegarde du résultat en csv
#A MODIFIER
df.to_csv('all_tweets_realDonaldTrump_sentiment_analisis.csv',index=False, encoding='utf-8-sig')

#Elaboration de graphique pour exploration de la donneé
# fig=px.histogram(df[df['subject']>0.5], x='polarity', color='polarity')
# fig=px.histogram(df[df['sentiment']>-1], x='polarity', color='polarity')
# fig.show()

