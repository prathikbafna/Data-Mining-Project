import tweepy
import json

# Set up your Twitter API credentials
consumer_key = "HRHWLEfeI0oBk71qXU5PR9FBc"
consumer_secret = "gQSLExrbrBmcsJDzUXM25dIPBf2gRbkq4URQmUPaT7keWgLbXq"
access_token = "1722457288579993600-eZ8lofV7qOvn8KQvCp7aSx2qfdyzZH"
access_token_secret = "pIPPR6fY3wXMa1M18YD2kTGwWBva3whAaMfwaD1oHvU7V"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the keyword you want to search for
keyword = "Apple"

# Search for tweets containing the keyword
tweets = api.search_tweets(q=keyword)

# Create a list to store the tweet data
tweet_data = []

# Iterate over the tweets
for tweet in tweets:
    # Get the user's follower count
    user_followers_count = tweet.user.followers_count
    
    # Creating a dictionary to store the tweet data
    tweet_info = {
        'source': 'twitter',
        'id': str(tweet.id),
        'text': tweet.full_text,
        'tag': tags,
        'sentiment': sentiment,
        'created_time': tweet.created_at,
        'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}",
        'spam': False,
        'misc': {
            'user_id': tweet.user.id_str,
            'user_name': tweet.user.screen_name,
            'user_followers_count': user_followers_count,
            'user_location': tweet.user.location,
            'user_verified': tweet.user.verified,
            'retweet_count': tweet.retweet_count,
            'favorite_count': tweet.favorite_count
        }
    }
    
 
    tweet_data.append(tweet_info)

 
with open('tweet_data.json', 'w') as file:
    json.dump(tweet_data, file)

print("Data saved to tweet_data.json")