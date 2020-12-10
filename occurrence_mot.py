#import des librairies
import csv
import pandas as pd
import re
import json 

#Fonction de suppression des éléments non utiles 
def remove_content(text):
    #Si le text est présent, on supprime les éléments inutiles
    if (text!=''):
        text = text.lower()
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        text = re.sub(r"https\S+", " ", text) #remove urls        
        text = re.sub(r"http\S+", "", text) #remove urls
        text=re.sub(r'\S+\.com\S+','',text) #remove urls
        text=re.sub(r'\@\w+','',text) #remove mentions
        text =re.sub(r'\#\w+','',text) #remove hashtags

        text = text.replace('t.co', ' ')
        text = text.replace('&amp', ' ')
        text =text.replace('\u201d','') #remove false quote
        text =text.replace('\u201c','') #remove false quote
    #Sinon, on met 0 pour éviter les erreurs
    else:
        text = 0
    return text



#Lecture du csv
df = pd.read_csv('fichiers/all_tweets_realDonaldTrump_cleaned.csv', encoding='utf8')
#creation d'un champ clean qui contiendra le texte à analyser
df['tweet_sans_residu']=df['tweet'].apply(lambda x: remove_content(x))
#Dans le champ date, on récupère le mois et l'année qui nous serviront ensuite à regrouper les tweets par mois
df['date_to_group']=df['date'].apply(lambda x:x[0:7])



#Regroupement des tweets par mois
final_cat_list = df['date_to_group'].unique()


#Liste vide qui contiendra les occurrences de mots par mois
word_count = {}

#Dans cette boucle, on compte le nombre d'occurrence pour chaque mois 
for f in final_cat_list:
    word_count[f] = {}
    message_list = list(df.loc[df['date_to_group'] == f, 'tweet_sans_residu'])
    for m in message_list:
        word_list = m.split(" ")
        for w in word_list:
            if w in word_count[f]:
                word_count[f][w] += 1
            else:
                word_count[f][w] = 1



#On sauvegarde enfin le résultat dans un json.
with open("fichiers/frequency_word_trump.json", "w",encoding='utf8') as outfile:  
    json.dump(word_count, outfile,ensure_ascii=False)

