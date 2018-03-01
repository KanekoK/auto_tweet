import sqlite3
import twitter
from random import randint
from datetime import datetime
from contextlib import closing
from config import CK, CS, AT, AS, twitter_id, DBNAME

from src.auto_follow import AutoFollow

if __name__ == '__main__':
    auto_follow = AutoFollow()

