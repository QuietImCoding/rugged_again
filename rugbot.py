import time, os
import tweepy

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

while True:
    res = api.search_tweets('@rugged_again', since_id=since_id)
    print([(s.id, s.text, s.user.screen_name) for s in res])
    if res != []:
        for status in res[::-1]:
            stext = status.text
            api.update_status(ruglines[status.id % len(ruglines)], in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
        since_id = res[0].id
    time.sleep(10)

