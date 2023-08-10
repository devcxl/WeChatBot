import sqlite3
import logging as log

class SQLiteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    def total(self, query, params=None):
        if params:
            result = self.fetch_one(query, params)
        else:
            result = self.fetch_one(query)
        return result[0] if result else 0

    def delete(self, query, params=None):
        if params:
            self.execute(query, params)
        else:
            self.execute(query)


class Model:
    db = None

    @classmethod
    def initialize(cls, db):
        cls.db = db

    @classmethod
    def create_table(cls):
        columns = ', '.join([f"{column} {data_type}" for column,
                            data_type in cls.__dict__.items() if not column.startswith('__')])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {cls.__name__} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns},create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        log.debug(f'{cls.__name__}: {create_table_query}')
        cls.db.execute(create_table_query)

    def save(self):
        columns = ', '.join(self.__dict__.keys())
        placeholders = ', '.join(['?' for _ in self.__dict__.values()])
        insert_query = f"INSERT INTO {self.__class__.__name__} ({columns}) VALUES ({placeholders})"
        values = tuple(self.__dict__.values())
        log.debug(f'{self.__class__.__name__}: {insert_query} {values}')
        self.db.execute(insert_query, values)

    def update(self):
        update_query = f"UPDATE {self.__class__.__name__} SET " + ', '.join(
            [f"{column} = ?" for column in self.__dict__.keys() if column != 'id']) + " WHERE id = ?"
        values = tuple(value for column, value in self.__dict__.items()
                       if column != 'id') + (self.id,)
        log.debug(f'{self.__class__.__name__}: {update_query} {values}')
        self.db.execute(update_query, values)

    def save_or_update(self):
        if hasattr(self, 'id') and self.id:
            self.update()
        else:
            self.save()

    def delete(self):
        delete_query = f"DELETE FROM {self.__class__.__name__} WHERE id=?"
        self.db.delete(delete_query, (self.id,))

    @classmethod
    def fetch_one(cls, where='1=1', params=None):
        sql = f"""SELECT * FROM {cls.__name__} WHERE {where}"""
        log.debug(f'{cls.__name__}: {sql} {params}')
        if params:
            result = cls.db.fetch_one(sql, params)
        else:
            result = cls.db.fetch_one(sql)

        if result:
            instance = cls()
            instance.__dict__.update(result)
            return instance
        else:
            return None

    @classmethod
    def total(cls, where='1=1', params=None):
        sql = f"""SELECT count(1) FROM {cls.__name__} WHERE {where}"""
        log.debug(f'{cls.__name__}: {sql} {params}')
        return cls.db.total(sql)

    @classmethod
    def fetch_all(cls, where='1=1', params=None):
        sql = f"""SELECT * FROM {cls.__name__} WHERE {where}"""
        log.debug(f'{cls.__name__}: {sql} {params}')
        if params:
            results = cls.db.fetch_all(sql, params)
        else:
            results = cls.db.fetch_all(sql)

        instances = []
        for result in results:
            instance = cls()
            instance.__dict__.update(result)
            instances.append(instance)

        return instances


class ChatGPTConfig(Model):
    email = "TEXT"
    password = "TEXT"
    access_token = "TEXT"
    proxy = "TEXT"


class ChatGPTChat(Model):
    name = "TEXT"
    conversation_id = "TEXT"
    parent_id = "TEXT"
    title = "TEXT"
    # SELECT conversation_id, parent_id, title FROM chat WHERE name='{chatname}';
    # UPDATE chat SET parent_id = '{parent_id}' WHERE conversation_id = '{conversation_id}';


class WeChatUser(Model):
    wechat_id = "TEXT"
    nick_name = "TEXT"
    user_name = "TEXT"
    marked_name = "TEXT"
    head_img = "TEXT"
    bg_img = "TEXT"
    content = "TEXT"
    ticket = "TEXT"
    raw = "TEXT"
    status = "INTEGER DEFAULT 0"
    # UPDATE user SET status = 1 WHERE wechat_id = '{wechat_id}';

class Message(Model):
    msg_id = "INTEGER"  # MsgId
    toUserName = "TEXT"  # NickName  # me
    fromUserName = "TEXT"  # ActualNickName # msg.user.NickName
    context = "TEXT"  # Text


if __name__ == "__main__":

    db = SQLiteDB('new.sqlite')
    Model.initialize(db)
    Message.create_table()
    flag = Message.fetch_one("msg_id = '123456'")
    # message = Message()
    # message.context = 'msg.text'
    # message.message_id = 'msg.MsgId'
    # message.toUserName = 'msg.NickName or ''ME'''
    # message.fromUserName = 'msg.ActualNickName or msg.user.NickName'
    # message.save()
