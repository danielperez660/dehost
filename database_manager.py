import sqlite3
from sqlite3 import OperationalError


class DBManager:
    def __init__(self):
        db = sqlite3.connect('statics.db')
        self.cursor = db.cursor()
        self.counter = self.counter_init()

        try:
            self.create_table()
        except OperationalError:
            print("Table Exists")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE WEBSITES(
            ID INT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            OWNER TEXT NOT NULL,
            CHAIN TEXT NOT NULL);
            """)

        print("Table Created")

    def add_website(self, name, owner, chain):
        self.cursor.execute("INSERT INTO WEBSITES VALUES (? ? ? ?)", (self.counter, name, owner, chain))
        self.counter += 1
        print("Added Successfully")

    def find_websites_for(self, user):
        self.cursor.execute("SELECT * FROM WEBSITES WHERE OWNER = ?", user)
        return self.cursor.fetchall()

    def counter_init(self):
        self.cursor.execute("select * from WEBSITES")
        total = len(self.cursor.fetchall())
        return total + 1
