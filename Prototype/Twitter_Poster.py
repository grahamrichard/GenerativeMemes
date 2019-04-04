from Twitter_Bot.Bot import Bot
from Markov_Object.Markov_Chain import Chain
from pathlib import Path
import json
import random
import os
import TwitterSQL as twit_sql
from datetime import datetime

before = datetime.now()

chars = 140
tries = 100
ratio = .5
handle = "Inspire_us"

# Geotag for Minneapolis
location = 23424977

# Finding filepath for twitter_credentials.json
base_path = Path("twitter_credentials.json").parent
file_path = (base_path / "../Prototype/Twitter_Bot/twitter_credentials.json").resolve()

with open(file_path) as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_TOKEN']
    access_secret = info['ACCESS_SECRET']

bot = Bot(consumer_key=consumer_key,
          consumer_secret=consumer_secret,
          access_key=access_key,
          access_secret=access_secret)

# From trends on twitter this creates a file in the form
# *trend*_tweets.txt that is later used for Markov and returns the file path
def make_trend():
    trend = ""
    for x in bot.get_trends(location).values():
        trend = x
        break

    tweet_list = bot.search_tweets(trend)
    with open(trend + '_tweets.txt', 'w+',encoding = "utf-8") as f:
        for tweet in tweet_list:
            f.write(tweet + "\n")

    file_name = trend + "_tweets.txt"

    base_path = Path(file_name).parent
    file_path = (base_path / file_name).resolve()
    return file_path


def make_tweet():
    tweet_list = bot.get_user_tweets(handle)
    with open(handle + '_tweets.txt', 'w+', encoding = "utf-8") as f:
        for tweet in tweet_list:
            f.write(tweet + "\n")
    file_name = handle + "_tweets.txt"
    base_path = Path(file_name).parent
    file_path = (base_path / file_name).resolve()
    return file_path

file_path = twit_sql.Query(handle)
# file_path = "query.txt"
after = datetime.now()
print("Time for checkpoint 1: "+after-before)
chain = Chain(chars=chars,
              tries=tries,
              ratio=ratio,
              filepath=file_path)

markov_tweet = chain.make_sent(1)

for chain in markov_tweet:
    bot.upload_text(chain)

os.remove(file_path)
after = datetime.now()

print("total time for program "+after-before)