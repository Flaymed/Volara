import random
import sqlite3
conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

def requestAlly(id, clanname):
    name = (clanname,)
    c.execute("SELECT name FROM kingdoms WHERE ownerid=?", id)
    requestsender = c.fetchone()
    c.execute("UPDATE kingdoms SET request=? WHERE name=?", [requestsender, name])
    conn.commit()

def isRequested(id):
    oid = (id,)
    c.execute("SELECT request FROM kingdoms WHERE ownerid=?", oid)
    results = c.fetchone()
    if results[0] == None:
        return False
    else:
        return results[0]

def hasAlly(clanname):
    name = (clanname,)
    c.execute("SELECT ally FROM kingdoms WHERE name=?", name)
    ally = c.fetchone()
    if ally[0] == None:
        return False
    else:
        return True

def addAlly(id, clanname):
    clan = (clanname,)
    c.execute("UPDATE kingdoms SET ally=? WHERE ownerid=?", [clan, id])
    c.execute("SELECT name FROM kingdoms WHERE ownerid=?", id)
    name = c.fetchone()
    c.execute("UPDATE kingdoms SET ally=? WHERE name=?", [name, clan])
    conn.commit()
    return True

def clearRequests(id):
    oid = (id,)
    c.execute("UPDATE kingdoms SET request=? WHERE ownerid=?", [None, oid])
    conn.commit()
    return "Requests Cleared!"

def checkAlly(id, clanname):
    oid = (id,)
    c.execute("SELECT ally FROM kingdoms WHERE ownerid=?", [oid])
    results = c.fetchone()
    if results[0] == clanname:
        return True
    else:
        return False

def removeAlly(id, clanname):
    oid = (id,)
    unally = (clanname,)
    c.execute("UPDATE kingdoms SET ally=? WHERE ownerid=?", [None, oid])
    c.execute("UPDATE kingdoms SET ally=? WHERE name=?", [None, unally])
    conn.commit()
    return "Sucessfully unallied {}".format(clanname)
