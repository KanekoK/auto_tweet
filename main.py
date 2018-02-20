import sqlite3
import twitter
from config import CK, CS, AT, AS, TWITTER_ID
from random import randint



auth = twitter.OAuth(consumer_key=CK,
                  consumer_secret=CS,
                  token=AT,
                  token_secret=AS)

t = twitter.Twitter(auth=auth)

print(t.followers.ids(user_id=TWITTER_ID))



