
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

path = './wine-reviews/winemag-data-130k-v4.csv'
data = pd.read_csv(path, index_col=0)

descriptions = defaultdict(list)
data.apply(lambda x: descriptions[x.country].append(x.description), axis=1)


unwanted_characters = re.compile('[^A-Za-z ]+')
for country in list(data.country.unique()):
    desc_string = ' '.join(descriptions[country])
    descriptions[country] = ' '.join([w.lower() for w in re.sub(unwanted_characters, ' ', desc_string).split() if len(w) > 3])

wine_stopwords = ['drink','wine','wines','flavor','flavors','note','notes','palate','finish','hint','hints','show','shows']
for w in wine_stopwords:
    STOPWORDS.add(w)


def generate_country_wordcloud(words, mask_image, filename=None, colormap='jet'):
    mask = np.array(Image.open(mask_image))
    wc = WordCloud(background_color="white", max_words=3000, mask=mask, stopwords=STOPWORDS, colormap=colormap)
    wc.generate(words)
    if filename:
        wc.to_file(filename)
    return wc

masks = dict()

masks['US'] = "./wordclouds/usa_template.png"
us_wc = generate_country_wordcloud(descriptions['US'], masks['US'], './wordclouds/US.jpg')
us_wc.to_image()
