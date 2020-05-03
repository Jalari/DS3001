import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from tfidf import TfIdf


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

   df['Aroma'] = aroma_feature
   return df


# remove empty and
def cleanData(wine):
    # drop columns
    wine.drop(columns=['taster_twitter_handle'], inplace=True)
    wine.drop(columns=['description'], inplace=True)
    # drop duplicates
    wine.drop_duplicates(inplace=True)
    # add "Unknown" to missing values in the categories with text
    wine.country.fillna("Unknown", inplace=True)
    wine.designation.fillna("Unknown", inplace=True)
    wine.province.fillna("Unknown", inplace=True)
    wine.region_1.fillna("Unknown", inplace=True)
    wine.region_2.fillna("Unknown", inplace=True)
    wine.taster_name.fillna("Unknown", inplace=True)
    wine.title.fillna("Unknown", inplace=True)
    # there is only one row with missing variety
    wine.drop(wine[wine.variety.isna()].index, inplace=True)

    # Get the median price per country and fill n/a price values based on their country
    wine['price'] = wine['price'].fillna(wine.groupby('country')['price'].transform('median'))

    # add total median price for Egypt and Tunisia since they have no value prices information for their countries
    wine['price'] = wine['price'].fillna(wine['price'].median())

    return wine


def main():
    path = './wine-reviews/winemag-data-130k-v2.csv'
    output =  './wine-reviews/winemag-data-130k-v4.csv'
    wine = pd.read_csv(path, index_col=0)
    print("Generating Aromas Column")
    wine = GenerateAromas(wine)
    print("Cleaning Dataset")
    wine = cleanData(wine)
    print("Saving to: " + output)
    wine.to_csv(output, mode='w', header=True)

if __name__ == '__main__':
    main()