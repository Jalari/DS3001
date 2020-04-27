import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from tfidf import TfIdf

# first time only to download nltk shit
# import nltk
# nltk.download()


# read raw data descriptions
data = pd.read_csv("./wine-reviews/winemag-data-130k-v2.csv")
description = data['description']

# load TFIDF
table = TfIdf()

#  Load bags of words
bagsofwords = pd.read_csv('./Primary_Aroma_BOW.csv')
for col in bagsofwords.columns:
    listofwords = bagsofwords[col].dropna()
    table.add_document(col,list_of_words=listofwords)

# track the new classes
aroma_feature = []

# remove stopwords
stop_words = set(stopwords.words('english'))

print("Doing calculations...")
for datapoint in description:

    # tokenize description
    words = word_tokenize(datapoint)
    wordsFiltered = []

    # remove stopwords
    for w in words:
        if w not in stop_words:
            wordsFiltered.append(w)

    # calc similarities
    sims = table.similarities(list_of_words=wordsFiltered)
    sims = np.array(sims)

    # check if any class was chosen
    if max(sims[:,1]) == '0.0':
        calced_feature = "Unknown"
    else:
        calced_feature = sims[sims[:, 1].argmax(axis=0),0]

    aroma_feature.append(calced_feature)

# write to file
print("Writing to file...")
data['Aroma'] = aroma_feature
data.drop('Unnamed: 0', axis=1, inplace=True)
data.drop('Unnamed: 0.1', axis=1, inplace=True)
data.to_csv('./wine-reviews/winemag-data-130k-v3.csv', mode='w',header=True)

