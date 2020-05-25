#!/usr/bin/env python
# coding: utf-8

# # HW1 : Data Science in Twitter Data

# **Required Readings:** 
# * Chapter 1 and Chapter 9 of the book [Mining the Social Web](https://www.safaribooksonline.com/library/view/mining-the-social/9781491973547/?orpq) 
# * The codes for Chapters 1 and 9 are in [here](https://github.com/mikhailklassen/Mining-the-Social-Web-3rd-Edition/tree/master/notebooks).
# 
# ** NOTE **
# * Please don't forget to save the notebook frequently when working in Jupyter Notebook, otherwise the changes you made can be lost.
# 
# *----------------------

# ## Data Collection: Download Twitter Data using API

# * As the first step of Data Science process, let's collect some twitter data. Choose a keyword and search tweets containing the keyword by using Twitter search API, and then download the searched tweets (including the meta data that the Search API returns) in a file. It is recommended that the number of searched tweets should be at least 300.
# * Store the tweets you downloaded into a local file (txt file or json file) 

# In[1]:


# What keyword did you choose?:  radio


# In[2]:


import twitter
import json


# ---------------------------------------------
# Define a Function to Login Twitter API
def oauth_login():
    # Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information
    # on Twitter's OAuth implementation.

    CONSUMER_KEY = 'ZUSLfZ2bScHKsfX55GFsyzie1'
    CONSUMER_SECRET = 'X0RvpqhbfVZRXXVSrvg1GyIqmVnrmIRxnT5LmqxwfZ4Xmrt3B9'
    OAUTH_TOKEN = '1087476712189898752-ZHASqkIhrWT78htUs57OGR2uIYORtr'
    OAUTH_TOKEN_SECRET = 'fzjSlOulj12AVZGfpWTf4jFnxgTHaVU9zcMK6Hx3FF7m0'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


# ----------------------------------------------
# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary
def tweet_search(api, query, max_tweets):
    ''' Function that takes in a search string 'query', the maximum
        number of tweets 'max_tweets', and the minimum (i.e., starting)
        tweet id. It returns a list of tweepy.models.Status objects. '''

    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)

        new_tweets = api.search(q=query, count=remaining_tweets)
        print('found', len(new_tweets), 'tweets')
        if not new_tweets:
            print('no tweets found')
            break
        searched_tweets.extend(new_tweets)

        return searched_tweets


search = tweet_search(api, "radio")

with open('twitter.json', 'w') as fp:
    json.dump(search, fp)





# ### Report  statistics about the tweets you collected 

# In[1]:


# The total number of tweets collected:  300


# # Data Exploration: Exploring the Tweets and Tweet Entities
# 
# **(1) Word Count:** 
# * Load the tweets you collected in the local file (txt or json)
# * compute the frequencies of the words being used in these tweets. 
# * Plot a table of the top 30 most-frequent words with their counts

# In[30]:


# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary














# ** (2) Find the most popular tweets in your collection of tweets**
# 
# Please plot a table of the top 10 most-retweeted tweets in your collection, i.e., the tweets with the largest number of retweet counts.
# 

# In[31]:


# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary












# **(3) Find the most popular Tweet Entities in your collection of tweets**
# 
# Please plot the top 10 most-frequent hashtags and top 10 most-mentioned users in your collection of tweets.

# In[32]:


# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary






# Plot a histogram of the number of user mentions in the list using the following bins.

# In[ ]:


bins=[0, 10, 20, 30, 40, 50, 100]

# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary




# 
#  ** (optional task for fun) Getting "All" friends (followees) and "All" followers of a popular user in the tweets**

# * choose a popular twitter user who has many followers in your collection of tweets.
# * Get the list of all friends and all followers of the twitter user.
# * Plot 20 out of the followers, plot their ID numbers and screen names in a table.
# * Plot 20 out of the friends (if the user has more than 20 friends), plot their ID numbers and screen names in a table.

# In[35]:


# Your code starts here
#   Please add comments or text cells in between to explain the general idea of each block of the code.
#   Please feel free to add more cells below this cell if necessary






# *-----------------
# # Done
# 
# All set! 
# 
# ** What do you need to submit?**
# 
# * **Notebook File**: Save this Jupyter notebook, and find the notebook file in your folder (for example, "filename.ipynb"). This is the file you need to submit. Please make sure all the plotted tables and figures are in the notebook.
# 
# ** How to submit: **
# 
#         Please submit through Canvas, in the Assignment "HW1".
#         
