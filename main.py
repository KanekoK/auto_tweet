import sqlite3
import twitter
from config import CK, CS, AT, AS, TWITTER_ID, DBNAME
from random import randint
from contextlib import closing


# Twitter情報
auth = twitter.OAuth(consumer_key=CK,
                  consumer_secret=CS,
                  token=AT,
                  token_secret=AS)

t = twitter.Twitter(auth=auth)


# フォロワーリスト取得
follower_lists = t.followers.ids(user_id=TWITTER_ID)

print(follower_lists)
profile = t.users.show(user_id=follower_lists["ids"][0])
print(profile)

# データベース接続
with closing(sqlite3.connect(DBNAME)) as conn:
    c = conn.cursor()

    conn.close()