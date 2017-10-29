import unittest
import tweepy
import requests
import json
from twitter_info import *


## SI 206 - HW
#Mia Bonanno
## COMMENT WITH:
## Your section day/time: Wed. 6-7pm
## Any names of people you worked with on this assignment:


## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.



## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing



## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points



## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.
CACHE_FNAME= "twitter_cached.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_data= cache_file.read()
    CACHE_D = json.loads(cache_data)
except:
    CACHE_D = {}


## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.
input_phrase= input("Enter Tweet term: ")
def get_tweets(input_phrase):

    if input_phrase in CACHE_D:
        twitter_data= CACHE_D[input_phrase] #gets data from the cache
    else:
        twitter_data= api.search(input_phrase)
        CACHE_D[input_phrase]=twitter_data
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_D))
        f.close()

    updated_data = twitter_data['statuses']
    return updated_data




## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!


#for tweets in get_tweets(input_phrase)[0:5]:

#    print (tweets)




## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.
with open("twitter_cached.json") as json_data:
    d=json.load(json_data)
    if input_phrase in d:
        print ('using cache')

        for tweet in d[input_phrase]['statuses'][0:5]:

            print ("TEXT: " + tweet['text'])
            print ("CREATED AT: " + tweet['created_at'] + '\n')

    else:
        print ('fetching')
        get_tweets(input_phrase)
        with open("twitter_cached.json") as json_data:
            d=json.load(json_data)
            for tweet in d[input_phrase]['statuses'][0:5]:

                print ("TEXT: " + tweet['text'])
                print ("CREATED AT: " + tweet['created_at'] + '\n')
