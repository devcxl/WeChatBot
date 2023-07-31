import sqlite3

class DB():

    def __init__(self, fileName) -> None:
        self.connect = sqlite3.connect(fileName)

    def execute(self, sql, params=None):
        cursor = self.connect.cursor()
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        cursor.close()
        self.connect.commit()

    def query_one(self, sql) -> any:
        cursor = self.connect.cursor()
        cursor.execute(sql)
        results = cursor.fetchone()
        cursor.close()
        return results

    def close(self):
        self.connect.close()

    def create_config_table(self):
        create_table = """
        CREATE TABLE config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT,
            access_token TEXT,
            proxy TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(create_table)

    def insert_config_data(self, email, password, access_token, proxy):
        insert = f"""
            INSERT INTO config (email, password, access_token, proxy)
            VALUES ('{email}', '{password}', '{access_token}','{proxy}');
        """
        self.execute(insert)

    def create_chat_table(self):
        create_table = """
        CREATE TABLE chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            conversation_id TEXT,
            parent_id TEXT,
            title TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(create_table)

    def insert_chat_data(self, name, conversation_id, parent_id, title):
        insert = f"""
        INSERT INTO chat (name,conversation_id,parent_id,title) 
        VALUES('{name}','{conversation_id}','{parent_id}','{title}');
        """
        self.execute(insert)

    def query_chat_data(self, chatname):
        query_sql = f"""SELECT conversation_id, parent_id, title FROM chat WHERE name='{chatname}';"""
        return self.query_one(query_sql)

    def update_chat_parent_id(self, conversation_id, parent_id):
        update = f"""UPDATE chat SET parent_id = '{parent_id}' WHERE conversation_id = '{conversation_id}';"""
        self.execute(update)

    def create_user_table(self):
        create_table = """
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wechat_id TEXT,
            nick_name TEXT,
            marked_name TEXT,
            head_img TEXT,
            bg_img TEXT,
            content TEXT,
            ticket TEXT,
            status INTEGER DEFAULT 0,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(create_table)

    def insert_user_data(self, wechat_id, nick_name, marked_name, head_img, bg_img, content, ticket):
        insert = f"""
        INSERT INTO user (wechat_id,nick_name,marked_name,head_img,bg_img,content,ticket)
        VALUES('{wechat_id}','{nick_name}','{marked_name}','{head_img}','{bg_img}','{content}','{ticket}');
        """
        self.execute(insert)

    def update_user_status(self, wechat_id):
        update = f"""UPDATE user SET status = 1 WHERE wechat_id = '{wechat_id}';"""
        self.execute(update)

