import sqlite3
from sqlite3 import OperationalError


class DBManager:
    def __init__(self):
        self.db = sqlite3.connect('statics.db', check_same_thread=False)
        self.cursor = self.db.cursor()

        try:
            self.__create_table()
            print("Table Created")
            self.db.commit()
        except OperationalError:
            print("Table Exists")

        self.counter = self.counter_init()

    def __create_table(self):
        self.cursor.execute("""
            CREATE TABLE WEBSITES(
            ID INT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            OWNER TEXT NOT NULL,
            CHAIN TEXT NOT NULL,
            LINK TEXT NOT NULL,
            CHAIN_LINK TEXT NOT NULL);
            """)

        print("Table Created")

    def add_website(self, name, owner, chain, link, chain_link):
        self.cursor.execute("INSERT INTO WEBSITES VALUES (?, ?, ?, ?, ?, ?)",
                            (self.counter, name, owner, chain, link, chain_link))
        self.counter += 1
        print("Added Successfully")
        self.db.commit()

    def find_websites_for(self, user):
        self.cursor.execute("SELECT * FROM WEBSITES WHERE OWNER = ?", (user,))
        return self.cursor.fetchall()

    def counter_init(self):
        self.cursor.execute("select * from WEBSITES")
        total = len(self.cursor.fetchall())
        return total + 1

    def find_website_name(self, name):
        self.cursor.execute("SELECT * FROM WEBSITES WHERE NAME = ?", (name,))
        return self.cursor.fetchall()
