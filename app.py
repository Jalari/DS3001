from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from numpy.linalg import norm
import scipy.spatial.distance as distance

app = Flask(__name__)

df = pd.read_csv('./wine-reviews/winemag-data-130k-v5.csv', delimiter=',',index_col = 0,header=0)
meta_headers = ['description','title','winery']

# Country headers organized by continent
europe_heaers = ['country_Austria','country_Bosnia and Herzegovina','country_Bulgaria', 'country_Croatia', 'country_Czech Republic','country_Cyprus','country_England', 'country_France','country_Germany', 'country_Greece', 'country_Hungary','country_Spain', 'country_Switzerland', 'country_Turkey', 'country_Portugal','country_Italy','country_Georgia','country_Serbia', 'country_Slovakia', 'country_Slovenia', 'country_Ukraine','country_Romania', 'country_Luxembourg', 'country_Macedonia',  'country_Moldova']
asia_headers=['country_Armenia','country_China', 'country_India']
na_headers=['country_Canada','country_US']
sa_headers=['country_Brazil', 'country_Chile','country_Mexico','country_Unknown']
oceania_headers=['country_Australia', 'country_New Zealand','country_Peru']
africa_headers=['country_Egypt','country_South Africa','country_Israel','country_Morocco', 'country_Lebanon']
country_headers = [na_headers,sa_headers,europe_heaers,africa_headers,asia_headers,oceania_headers]

# aroma headers organized by question
fruity = ['aroma_Dried Fruit','aroma_Red Fruit']
earthy=['aroma_Earth', 'aroma_Flower', 'aroma_Noble Rot','aroma_Vegetable']
tropical=['aroma_Citrus','aroma_Tropical Fruit','aroma_Tree Fruit']
other=['aroma_Spice','aroma_Unknown', ]
aroma_header=[fruity,earthy,tropical,other]

meta_data = df.filter(meta_headers, axis=1).to_numpy()


df.drop(meta_headers, axis=1, inplace=True)
header = list(df.columns.values)
df = df.to_numpy()

df = df.astype(dtype=int)


# TODO before going live
# https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/


@app.route('/index.html', methods=['GET', 'POST','DELETE', 'PATCH'])
@app.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        QuestionaireAnswers = request.form.to_dict()

        # todo setup handle on the index page only
        ideal_vector = header.copy()
        print(QuestionaireAnswers)

        # change points to 90
        ideal_vector[0] = 90
        # update price
        ideal_vector[1] = int(QuestionaireAnswers['price'])
        # update country
        for i in country_headers[ int(QuestionaireAnswers['country'])]:
            ideal_vector[header.index(i)] = 1

        #     updaet variety
        ideal_vector[header.index('variety_' + QuestionaireAnswers['variety'])] = 1
        # updaate aroma
        for i in country_headers[ int(QuestionaireAnswers['aroma'])]:
            ideal_vector[header.index(i)] = 1

        # set all other values to 0
        for ind,val in enumerate(ideal_vector):
            if type(val) != int:
                ideal_vector[ind] = 0

        ideal_vector = np.asarray(ideal_vector)

        print("This was the given Ideal Vector: ")
        print(ideal_vector)

        distances = []

        # compute cosine similarity between points
        for i in df:
            a = ideal_vector
            b = i
            cos_sim = 1 - np.dot(a, b)/(norm(a)*norm(b))
            distances.append(cos_sim)

        # find best similarity
        min_indexes = np.argsort(distances)[:5]


        for index in min_indexes:
            # print(min_indexes)
            # max_index = distances.index(min(distances))
            #
            print("This was the closest wine: " + str(meta_data[index,1]))

            print("This was the closest wine's vector: ")
            print(df[index,:])



    return render_template('index.html')


@app.route('/results.html', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        QuestionaireAnswers = request.form.to_dict()

        # todo make this on client side
        ideal_vector = header.copy()
        print(QuestionaireAnswers)

        # change points to 90
        ideal_vector[0] = 90
        # update price
        ideal_vector[1] = int(QuestionaireAnswers['price'])
        # update country
        for i in country_headers[ int(QuestionaireAnswers['country'])]:
            ideal_vector[header.index(i)] = 1

        #     updaet variety
        ideal_vector[header.index('variety_' + QuestionaireAnswers['variety'])] = 1
        # updaate aroma
        for i in country_headers[ int(QuestionaireAnswers['aroma'])]:
            ideal_vector[header.index(i)] = 1

        # set all other values to 0
        for ind,val in enumerate(ideal_vector):
            if type(val) != int:
                ideal_vector[ind] = 0

        ideal_vector = np.asarray(ideal_vector)

        print("This was the given Ideal Vector: ")
        print(ideal_vector)

        distances = []

        # compute cosine similarity between points
        for i in df:
            a = ideal_vector
            b = i
            cos_sim = 1 - np.dot(a, b)/(norm(a)*norm(b))
            distances.append(cos_sim)

        # find best similarity
        min_indexes = np.argsort(distances)[:5]


        for index in min_indexes:
            # print(min_indexes)
            # max_index = distances.index(min(distances))
            #
            print("This was the closest wine: " + str(meta_data[index,1]))

            print("This was the closest wine's vector: ")
            print(df[index,:])

    return render_template('results.html')


'''
todo

compute euclidian distance of new data between the dataset

np.sqrt(np.sum((given_vector - other_vector) ** 2))

find the closest datapoint

return closest datapoint to be used in recomender


'''


if __name__ == '__main__':
    app.run()