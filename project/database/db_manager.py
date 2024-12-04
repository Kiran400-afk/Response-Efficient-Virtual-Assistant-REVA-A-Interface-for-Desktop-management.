```python
import sqlite3
import mysql.connector
from pymongo import MongoClient
from typing import Any, List, Dict, Optional
from config import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION, MYSQL_CONFIG, SQLITE_DB_PATH

class DatabaseManager:
    def __init__(self):
        self.sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
        self.mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        self.mongo_client = MongoClient(MONGODB_URI)
        self.mongo_db = self.mongo_client[MONGODB_DB]
        self.create_tables()

    def create_tables(self):
        cursor = self.sqlite_conn.cursor()
        cursor.execute()
        cursor.execute()
        self.sqlite_conn.commit()

    def execute_mysql_query(self, query: str) -> List[Any]:
        cursor = self.mysql_conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            raise Exception(f"MySQL Error: {err}")
        finally:
            cursor.close()

    def execute_mongodb_query(self, query: Dict) -> Optional[Dict]:
        collection = self.mongo_db[MONGODB_COLLECTION]
        try:
            return collection.find_one(query)
        except Exception as e:
            raise Exception(f"MongoDB Error: {e}")

    def store_command(self, command: str):
        cursor = self.sqlite_conn.cursor()
        cursor.execute("INSERT INTO command_history (command) VALUES (?)", (command,))
        self.sqlite_conn.commit()

    def get_user_preferences(self) -> Dict:
        cursor = self.sqlite_conn.cursor()
        cursor.execute("SELECT preferences FROM user_info ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        return eval(result[0]) if result and result[0] else {}

    def close_connections(self):
        self.sqlite_conn.close()
        self.mysql_conn.close()
        self.mongo_client.close()
```