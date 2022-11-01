import datetime
import pandas as pd
import sqlite3
import telegram

DB_PATH = 'data.db'


class Sql:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(DB_PATH)

    def close(self):
        self.conn.close()

    def insert(self, table, values):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(f"insert into {table} values ({','.join(['?' for x in range(len(values))])})", tuple(values))
        self.conn.commit()
        self.close()

    def update(self, table, values):
        self.connect()
        cur = self.conn.cursor()
        cur.execute(f"""update {table} 
                        set {','.join([f'{x.col}={x.value}' for x in values])}
                        where id = ?""", tuple(values))
        self.conn.commit()
        self.close()

    def data_frame_to_table(self, df: pd.DataFrame):
        self.connect()
        df.to_sql(df.name, self.conn, if_exists='replace')
        self.conn.commit()
        self.close()


class Data:
    def __init__(self):

        self.user_data = []


    def register_new_user(self, tg_user: telegram.user):
        user = User(tg_user)


class User:
    def __init__(self, tg_user: telegram.user):
        # telegram user id
        self.id = tg_user.id
        self.name = tg_user.name
        # date user joined group
        self.join_date = datetime.datetime.utcnow()
        # user type
        # 0: owner, 1: admin, 2: bot
        # 10: normal user
        # 20: free user
        self.type = '10'
        # user state
        # 0: in group, 1: not in group, 2: black list
        self.state = '0'
        # payment records
        self.records = [Record()]

        self.comment = ''
        self.update_user = 'bot'
        self.create_user = 'bot'
        self.update_date = datetime.datetime.utcnow()
        self.create_date = datetime.datetime.utcnow()


class Record:
    def __init__(self):
        self.id = ''
        self.date = datetime.datetime.utcnow()
        # payment type
        # 0: monthly, 1: quarterly, 2: yearly
        self.type = 0
        self.amount = 0
        self.expired_date = ''
        self.confirmed = False

        self.comment = ''
        self.update_user = ''
        self.create_user = ''
        self.update_date = ''
        self.create_date = ''
