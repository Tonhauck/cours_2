#impot des librairies
import csv
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re

#Fonction de suppression des éléments non utiles 
def remove_content(text):

    text = text.lower()
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())
    text = re.sub(r"https\S+", " ", text) #remove urls
    text = text.replace('t.co', ' ')
    text = text.replace('&amp', ' ')
    text = re.sub(r"http\S+", " ", text) #remove urls
    text=re.sub(r'\S+\.com\S+',' ',text) #remove urls
    text=re.sub(r'\@\w+',' ',text) #remove mentions
    text =re.sub(r'\#\w+',' ',text) #remove hashtags	

    return text

#Fonction de nettoyage des tweets 
def process_text(text): #clean text
	clean = ''
	text=remove_content(text)

    #Découpage des phrases en mot (token)
	text = re.sub('[^A-Za-z]', ' ', text.lower()) #remove non-alphabets
	tokenized_text = nltk.word_tokenize(text) #tokenize
	#Déclaration des stops words dans une variable
	stop_words = stopwords.words('english')
	#Par cette méthode, on garde supprime les mots présents dans la liste des stop words 
	#et on élimine ainsi tous les petits mots parasites (the, is, an, and...)
	clean_text = [
	word for word in tokenized_text
	if word not in stop_words ] 
	if len(clean_text) > 0:
	    clean = ' '.join(clean_text)
	else:
	    clean = '_'

	return clean




#lecture du csv 
# A MODIFIER
df = pd.read_csv('fichiers/all_tweets_realDonaldTrump.csv')
#creation d'un champ clean contenant le text stemminisé
df['cleaned_tweets']=df['tweet'].apply(lambda x: process_text(x))
#sauvegarde du csv
#A MODIFIER
df.to_csv('fichiers/all_tweets_realDonaldTrump_cleaned.csv', index=False, encoding='utf-8-sig',quotechar='"',
                     quoting=csv.QUOTE_NONNUMERIC)
