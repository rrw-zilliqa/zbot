import peewee

db = peewee.SqliteDatabase("accounts.db")

class User(peewee.Model):
    class Meta:
        database = db
