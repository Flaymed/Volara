import random
import sqlite3
conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

#Raid constants
goldSteal = 0.5
populationDecrease = 0.15
offenseLose = 5
defenseLose = 10
offenseIncrease = 4
defenseIncrease = 8

#Table Structure:
#owner VARCHER, ownerid INT, name VARHCAR, rank INT, attack INT, defense INT, vision INT, gold INT, population INT

def raid(name, clan):


    #Get stats on raiding kingdom

    oname = (name,) #sanitize input
    c.execute("SELECT * FROM kingdoms WHERE owner=?", oname)
    data1 = c.fetchone()
    clanOneAttack = data1[4]
    clanOneDefense = data1[5]
    clanOneVision = data1[6]
    clanOneGold = data1[7]
    clanOnePopulation = data1[8]

    #Get Stats on defending kingdom

    clanname = (clan,) #sanitize input
    c.execute("SELECT * FROM kingdoms WHERE name=?", clanname)
    data2 = c.fetchone()
    clanTwoAttack = data2[4]
    clanTwoDefense = data2[5]
    clanTwoVision = data2[6]
    clanTwoGold = data2[7]
    clanTwoPopulation = data2[8]

    #Compare data

    if clanOneAttack > clanTwoDefense:
        #Loses Raid
        newClanTwoPopulation = clanTwoPopulation * populationDecrease
        clanTwoGold = clanTwoGold * goldSteal
        clanTwoVision = clanTwoVision - 5
        clanTwoAttack = clanTwoAttack - offenseLose
        clanTwoDefense = clanTwoDefense - defenseLose

        c.execute("UPDATE kingdoms SET attack=?, defense=?, vision=?, gold=?, population=? WHERE name=?", [clanTwoAttack, clanTwoDefense, clanTwoVision, clanTwoGold, newClanTwoPopulation, clanname])

        #Wins raid
        clanOneAttack = clanOneAttack + offenseIncrease
        clanOneDefense = clanOneDefense + defenseIncrease
        clanOneVision = clanOneVision + 5
        clanOneGold = clanOneGold + clanTwoGold
        clanOnePopulation = clanOnePopulation + (clanTwoPopulation - newClanTwoPopulation)

        c.execute("UPDATE kingdoms SET attack=?, defense=?, vision=?, gold=?, population=? WHERE owner=?", [clanOneAttack, clanOneDefense, clanOneVision, clanOneGold, clanOnePopulation, oname])

        #Commit changes to db
        conn.commit()
