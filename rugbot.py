import time, os
import tweepy
from datetime import datetime

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

since_id = 0
res = api.search_tweets('@rugged_again', count=1)
since_id = res[0].id

with open('rugphrases.txt', 'r') as rugfile:
    ruglines = rugfile.readlines()

with open('gms.txt', 'r') as gmfile:
    gms = gmfile.readlines()

while True:
    ctime = datetime.now()
    if ctime.hour == 7 + (since_id % 4) and ctime.minute == since_id % 60 and ctime.second < 10:
        api.update_status(gms[since_id % len(gms)])
    res = api.search_tweets('@rugged_again', since_id=since_id)
    print([(s.id, s.text, s.user.screen_name) for s in res])
    if res != []:
        for status in res[::-1]:
            if status.user.screen_name != 'rugged_again':
                stext = status.text
                api.update_status(ruglines[status.id % len(ruglines)], in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
        since_id = res[0].id
    time.sleep(10)

