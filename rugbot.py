import time, os, dateutil.tz, re
import tweepy, requests
from datetime import datetime
import random

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
except:
    print("Auth error :'(")

since_id = 0
try:
    res = api.search_tweets('@rugged_again', count=1)
    since_id = res[0].id
except:
    print('Unable to search... rate limit reached?')

with open('rugphrases.txt', 'r') as rugfile:
    ruglines = rugfile.readlines()

with open('gms.txt', 'r') as gmfile:
    gms = gmfile.readlines()

with open('lastcommit.txt', 'r') as lcfile:
    lastcommit = lcfile.read()

try:
    rex = r'.*href="/QuietImCoding/rugged_again/commit[^>]*>([^<]*).*'
    res = requests.get('https://github.com/QuietImCoding/rugged_again/commits/main')
    matches = re.findall(rex, res.text)
    if matches[0] != lastcommit:
        api.update_status("RugBot has received an update from the central data processor... found the following text in subconcious memory: " +
                          matches[0])
        lastcommit = matches[0]
        with open('lastcommit.txt', 'w') as lcoutfile:
            lcoutfile.write(lastcommit)
except:
    print("Error fetching / tweeting commit message...")

while True:
    ctime = datetime.now(dateutil.tz.gettz("PST"))
    if ctime.hour == 7 + (since_id % 4) and ctime.minute == since_id % 60 and ctime.second < 3:
        api.update_status(gms[since_id % len(gms)])
    res = api.search_tweets('@rugged_again', since_id=since_id)
    updated = [(s.id, s.text, s.user.screen_name) for s in res]
    if updated != []:
        print(f'Activity : {updated}')
    if res != []:
        for status in res[::-1]:
            if status.user.screen_name != 'rugged_again':
                stext = status.text
                try:
                    api.update_status(ruglines[status.id % len(ruglines)], in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
                except Exception as e:
                    print(f'{e}, {status}')
        since_id = res[0].id
    time.sleep(random.randint(0, 5) + 5)

