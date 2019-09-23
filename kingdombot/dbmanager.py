import random
import sqlite3
conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

def onReady():
    c.execute("CREATE TABLE IF NOT EXISTS kingdoms(owner VARCHER, ownerid INT, name VARHCAR, rank INT, attack INT, defense INT, vision INT, gold INT, population INT)")
    conn.commit()

def wipeDB():
    c.execute("DROP TABLE kingdoms")
    conn.commit()

def checkOwner(id):
    ownerId = (str(id),)
    c.execute("SELECT * FROM kingdoms WHERE ownerid=?", ownerId)
    result = c.fetchone()
    if result == None:
        return False
    else:
        return True

def checkExist(name):
    kname = (str(name),)
    c.execute("SELECT * FROM kingdoms WHERE name=?", kname)
    result = c.fetchone()
    if result == None:
        return False
    else:
        return True

def createKingdom(name, owner, ownerid):
    Kname = (str(name),)
    Kowner = (str(owner),)
    Kownerid = (int(ownerid),)
    c.execute("INSERT INTO kingdoms (owner, ownerid, name, rank, attack, defense, vision, gold, population) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [owner, ownerid, name, 0, 10, 10, 20, 100, 450])
    conn.commit()

def ownsKingdom(id):
    cid = (str(id),)
    c.execute("SELECT * FROM kingdoms WHERE ownerid=?", cid)
    result = c.fetchone()
    if result == None:
        return False
    else:
        return True

def checkKingdomOwner(name, id):
    testid = (int(id),)
    c.execute("SELECT * FROM kingdoms WHERE ownerid=?", testid)
    result = c.fetchone()
    if result[2] == name:
        return True
    else:
        return False

def deleteKingdom(name):
    Kname = (str(name),)
    c.execute("DELETE FROM kingdoms WHERE name=?", Kname)
    conn.commit()

def goldTop():
    c.execute("SELECT * FROM kingdoms ORDER BY gold ASC")
    results = c.fetchall()
    gold = []
    for result in results:
        gold.append(result[7])
    return gold

def goldTopName():
    c.execute("SELECT * FROM kingdoms ORDER BY gold ASC")
    results = c.fetchall()
    name = []
    for result in results:
        name.append(result[2])
    return name

def mine():
    gold = random.randint(2, 100)
    return gold

def addGold(id, gold):
    ownerid = (int(id),)
    c.execute("SELECT gold FROM kingdoms WHERE ownerid=?", ownerid)
    currentgold = c.fetchone()
    addedgold = gold
    print(currentgold)
    print(addedgold)
    newgold = currentgold + addedgold
    c.execute("UPDATE kingdoms SET gold=? WHERE ownerid=?", [int(newgold), ownerid])
