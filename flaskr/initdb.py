# 程序数据库生成和初始化脚本
import sqlite3
from contextlib import closing

DATABASE = 'flaskr.db'


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with open('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_db()
