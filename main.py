import sqlite3
import twitter
from config import CK, CS, AT, AS, twitter_id, DBNAME
from random import randint
from contextlib import closing


# SQLite、twitter_listsテーブルに接続
# データベース接続
def get_last_twitter_id():
    last_twitter_id = 0;
    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()
    # id列の数が一番大きいtwitter_idを取得
        sql = '''
        SELECT twitter_id
        FROM twitter_lists
        WHERE id = (
            SELECT MAX(id)
            FROM twitter_lists
        )
        '''
        for row in c.execute(sql):
            last_twitter_id = row

    return last_twitter_id[0]

twitter_id = get_last_twitter_id();
profile = ""

# Twitter情報
auth = twitter.OAuth(consumer_key=CK,
                  consumer_secret=CS,
                  token=AT,
                  token_secret=AS)

t = twitter.Twitter(auth=auth)
# フォロワーリスト取得
follower_lists = t.followers.ids(user_id=twitter_id, count=5)
# 取得したidのフォロワーが5つ取得できるかどうか
if len(follower_lists["ids"]) >= 5:
    # SQLiteに入れる
    for follower_list in follower_lists["ids"]:
        profile = t.users.show(user_id=follower_list)
        print(profile)
else:
    # id列から-1をする
    pass
