
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
from PIL import Image
from os import path

#lecture du csv
df = pd.read_csv('fichiers/all_tweets_realDonaldTrump_cleaned.csv')
#champs clean => liste de mot
temp=' '.join(df['cleaned_tweets'].tolist())
#importation du png qui servira pour le mask (N&B)
wine_mask = np.array(Image.open("img/trump.png"))

#reshape du mask pour éviter les erreur de géométrie et améliorer la détection de la figure
wine_mask = wine_mask.reshape((wine_mask.shape[0],-1), order='F')
#Remplacement des 0 par 255 pour créer le masque à l'intérieur duquel seront placé les mots
wine_mask[wine_mask == 0] = 255
# # Transformation du mask en un tableau :
transformed_wine_mask = np.ndarray((wine_mask.shape[0],wine_mask.shape[1]), np.int32)

# Create a word cloud image
wc = WordCloud(width=1000,height=1000, background_color="white", max_words=1000, mask=wine_mask, 
	 contour_width=10,min_font_size = 10, contour_color='firebrick')
# Generate a wordcloud
wc.generate(temp)

# store to file
wc.to_file("trump_word.png")

# show
plt.figure(figsize=[10,10])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()


