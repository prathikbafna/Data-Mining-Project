 
import tweepy
import json

# Set up your Twitter API credentials
consumer_key = "HRHWLEfeI0oBk71qXU5PR9FBc"
consumer_secret = "gQSLExrbrBmcsJDzUXM25dIPBf2gRbkq4URQmUPaT7keWgLbXq"
access_token = "1722457288579993600-eZ8lofV7qOvn8KQvCp7aSx2qfdyzZH"
access_token_secret = "pIPPR6fY3wXMa1M18YD2kTGwWBva3whAaMfwaD1oHvU7V"

# Set up the keyword you want to search for
keyword = "Apple"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the number of tweets you want to retrieve
num_tweets = 100

# Retrieve tweets based on the keyword
tweets = api.search_tweets(q=keyword, count=num_tweets)

# Store tweets in a JSON file
data = []
for tweet in tweets:
    data.append(tweet._json)

with open('tweets.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Tweets retrieved and stored in tweets.json file.")
