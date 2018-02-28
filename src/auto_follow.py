import sqlite3
import twitter
from random import randint
from datetime import datetime
from contextlib import closing
from config import CK, CS, AT, AS, twitter_id, DBNAME

##### TODO ######

# ・ リストの名前にlistはつけない

################

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
            WHERE protected = 0
        )
        '''
        for row in c.execute(sql):
            last_twitter_id = row

    return last_twitter_id[0]


def get_id_list():
    with closing(sqlite3.connect(DBNAME)) as conn:
        id_list = []
        c = conn.cursor()
        sql = '''
            SELECT twitter_id FROM twitter_lists
        '''
        for one_id in c.execute(sql):
            id_list.append(one_id[0])
        return id_list
        conn.close()


def id_to_user_info(user_id):
    protected_convert = 0
    user_info = api.users.show(user_id=user_id)

    if user_info["protected"]:
        protected_convert = 1 # TRUE
    else:
        protected_convert = 0 # FALSE
    return (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_info["id"],
            user_info["screen_name"],
            user_info["name"],
            user_info["description"],
            user_info["location"],
            protected_convert,
            "unilaterally",
        )




# TODO クラスにする
last_twitter_id = get_last_twitter_id();
user_infomation = ""
user_info_list = []

# Twitter情報
auth = twitter.OAuth(consumer_key=CK,
                  consumer_secret=CS,
                  token=AT,
                  token_secret=AS)

api = twitter.Twitter(auth=auth)

# フォロワーリスト取得
follower_ids = api.followers.ids(user_id=last_twitter_id, count=5)["ids"]

# 取得したidのフォロワーが5件取得できるかどうか

if len(follower_ids) >= 5:
    # TODO: 一件ずつデータ重複がないか検索する
    follower_ids = set(follower_ids)-set(get_id_list())
    user_infos = [ id_to_user_info(follower_id) for follower_id in follower_ids ]
else:
    # TODO
    # id列から-1をする
    pass

# TODO
if len(follower_ids) > 0:
    for follower_id in follower_ids:
        api.friendships.create(user_id=follower_id)
    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()
        # SQLiteに入れる
        sql = '''
            INSERT INTO twitter_lists(
                datetime,
                twitter_id,
                user_id,
                user_name,
                profile,
                location,
                protected,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        c.executemany(sql, user_infos)
        conn.commit()



    conn.close()


