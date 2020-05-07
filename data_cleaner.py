import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import names
import random

class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0

        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a
list of words.
        """

        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                      doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])

        return sims


# read description of the dataset to obtain aromas feature
def GenerateAromas(df):
   description = df['description']
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

   df['aroma'] = aroma_feature
   return df

# Generate a matrix of random reviews per wine nad taster
def gen_ratingMatrix(wine,numtasters):
    output =  './wine-reviews/reviews.csv'

    tasters = []

    for taster in range(numtasters):
        tasters.append(names.get_full_name())


    wine_names = wine['title'].unique()

    # generate random reviews
    rand_wine = pd.DataFrame(np.random.randint(80, 99,size=(len(wine_names),numtasters)), columns=tasters,index=wine_names)

    for col in rand_wine.columns:
        rand = random.uniform(0.1, 0.8)
        rand_wine.loc[rand_wine.sample(frac=rand).index, col] = pd.np.nan


    rand_wine.to_csv(output, mode='w', header=True)



# remove empty and
def cleanData(wine):

    # drop columns
    wine.drop(columns=['taster_twitter_handle','province','taster_name','region_1','region_2','designation'], inplace=True)

    # drop duplicates
    wine.drop_duplicates(inplace=True)

    # Get the median price per country and fill n/a price values based on their country
    wine['price'] = wine['price'].fillna(wine.groupby('country')['price'].transform('median'))

    # add total median price for Egypt and Tunisia since they have no value prices information for their countries
    wine['price'] = wine['price'].fillna(wine['price'].median())

    # add "Unknown" to missing values in the categories with text
    wine.fillna("Unknown", inplace=True)

    # there is only one row with missing variety
    wine.drop(wine[wine.variety.isna()].index, inplace=True)

    # Clean varieties to only 4 types
    wine.loc[wine['variety'].str.contains('Pinot Noir', case=False), 'variety'] = 'PinotNoir'
    wine.loc[wine['variety'].str.contains('Chardonnay', case=False), 'variety'] = 'Chardonnay'
    wine.loc[wine['variety'].str.contains('Cabernet Sauvignon', case=False), 'variety'] = 'CabernetSauvignon'
    wine.loc[wine['variety'].str.contains('Red Blend', case=False), 'variety'] = 'RedBlend'
    wine.loc[~wine['variety'].str.contains('PinotNoir') & ~wine['variety'].str.contains('Chardonnay')& ~wine['variety'].str.contains('CabernetSauvignon')& ~wine['variety'].str.contains('RedBlend'),'variety'] = 'Other'

    # One hot encode nominal data
    wine = pd.get_dummies(data=wine,columns=['aroma','country','variety'], drop_first=True)

    return wine


def main():
    path = './wine-reviews/winemag-data-130k-v2.csv'
    output =  './wine-reviews/winemag-data-130k-v5.csv'
    wine = pd.read_csv(path, index_col=0)

    print("Generating Review Matrix")
    gen_ratingMatrix(wine,200)


    print("Generating Aromas Column")
    wine = GenerateAromas(wine)
    print("Cleaning Dataset")
    wine = cleanData(wine)
    print("Saving to: " + output)
    wine.to_csv(output, mode='w', header=True)

if __name__ == '__main__':
    main()