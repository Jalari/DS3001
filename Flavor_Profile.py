
# Typical imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

# Not so typical
import matplotlib.image as image
import matplotlib.colors
from collections import defaultdict
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from IPython.display import Image as im
import squarify as sq

data = pd.read_csv('./wine-reviews/winemag-data-130k-v3.csv', index_col=0)
countries = data.country.value_counts()

# Limit top countries to those with more than 500 reviews
temp_dict = countries[countries>500].to_dict()
temp_dict['Other'] = countries[countries<501].sum()
less_countries = pd.Series(temp_dict)
less_countries.sort_values(ascending=False, inplace=True)

# Turn Series into DataFrame for display purposes
df = less_countries.to_frame()
df.columns=['Number of Reviews']
df.index.name = 'Country'


# New colors for tree map since base ones are bland
cmap = plt.cm.gist_rainbow_r
norm = matplotlib.colors.Normalize(vmin=0, vmax=15)
colors = [cmap(norm(value)) for value in range(15)]
np.random.shuffle(colors)

# Use squarify to plot the tree map with the custom colors
fig,ax = plt.subplots(1,1,figsize=(11,11))
sq.plot(sizes=less_countries.values, label=less_countries.index.values, alpha=0.5, ax=ax, color=colors)
plt.axis('off')
plt.title('Countries by Number of Wine Reviews')
plt.show()


descriptions = defaultdict(list)
data.apply(lambda x: descriptions[x.country].append(x.Aroma), axis=1)


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

masks['US'] = "./wordcloud_templates/usa39.png"
us_wc = generate_country_wordcloud(descriptions['US'], masks['US'], './wordclouds/US_flavor.jpg')
us_wc.to_image()
