import sqlite3
import twitter
from random import randint
from datetime import datetime
from contextlib import closing
from config import CK, CS, AT, AS, twitter_id, DBNAME

##### TODO ######

# リストの名前にlistはつけない

################

class AutoFollow:

    def __init__(self) -> None:
        # Twitter情報
        self.auth = twitter.OAuth(
            consumer_key=CK,
            consumer_secret=CS,
            token=AT,
            token_secret=AS
        )
        self.api = twitter.Twitter(auth=self.auth)

    # DBのtwitte_listsテーブルからラストのid番号を取得
    def get_last_twitter_id():
        last_twitter_id = 0;
        with closing(sqlite3.connect(DBNAME)) as conn:
            c = conn.cursor()
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


    # DBのtwitte_listsテーブルから全てのidリストを取得
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


    # ツイッターのidを渡すとそのidのユーザーの詳細を返す（api）
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


    def duplication_check(count=5):
        # フォロワーリスト取得
        last_twitter_id = get_last_twitter_id();
        follower_ids = api.followers.ids(user_id=last_twitter_id, count=count)["ids"]

        # 取得したidのフォロワーが5件取得できるかどうか
        if len(follower_ids) >= 5:
            # TODO: 一件ずつデータ重複がないか検索する
            follower_ids = set(follower_ids)-set(get_id_list())
            user_infos = [ id_to_user_info(follower_id) for follower_id in follower_ids ]
        else:
            # TODO
            # id列から-1をする
            pass
        return user_infos


    def follow_and_record(follower_ids, user_infos):
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











