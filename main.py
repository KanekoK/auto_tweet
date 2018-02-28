import sqlite3
import twitter
from config import CK, CS, AT, AS, twitter_id, DBNAME
from random import randint
import datetime
from contextlib import closing


# Twitter情報
auth = twitter.OAuth(consumer_key=CK,
                  consumer_secret=CS,
                  token=AT,
                  token_secret=AS)

api = twitter.Twitter(auth=auth)



now = datetime.datetime.now()
before_fourday = (now - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
before_fiveday = (now - datetime.timedelta(days=4)).strftime("%Y-%m-%d")
before_fiveday_followred = []
with closing(sqlite3.connect(DBNAME)) as conn:
    c = conn.cursor()
    sql = '''
        SELECT *
        FROM twitter_lists
        WHERE datetime > ? AND datetime < ?
    '''
    day_term = [before_fourday, before_fiveday]

    # 5日前にフォローしたリストを取得
    for row in c.execute(sql, day_term):
        before_fiveday_followred.append(row)
    # 取得したidから自分をフォローしているか
    for followred_id in before_fiveday_followred:
        followred_id_list = api.friends.ids(user_id=followred_id[2])
        if twitter_id in followred_id_list["ids"]:
            sql = '''
                UPDATE twitter_lists
                SET status = "mutual"
                WHERE id = ?
            '''
            c.execute(sql, [(followred_id[0])])
            conn.commit()
        else:
            sql = '''
                UPDATE twitter_lists
                SET status = "disconnected"
                WHERE id = ?
            '''
            c.execute(sql, [(followred_id[0])])
            api.friendships.destroy(user_id=followred_id[2])
            conn.commit()

