import random
import sqlite3
conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

def raid(name, clan):
    name = (name,)
    c.execute("SELECT * FROM kingdoms WHERE owner=?", name)
    result = c.fetchone()
    print(result[2])

raid("Flaymed", "WithersUnited")
