import os

from peewee import SqliteDatabase

db = SqliteDatabase("hands.db")

print("Working directory:", os.getcwd())
print("Database path:", db.database)
print("Absolute database path:", os.path.abspath(db.database))