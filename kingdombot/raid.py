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

        return "{}\'s clan has defeated: {}".format(name, clan)

    elif clanOneAttack == clanTwoDefense:

        #clan 2
        clanTwoDefense = clanTwoDefense + 5
        clanTwoVision = clanTwoVision + 5

        c.execute("UPDATE kingdoms SET defense=?, vision=? WHERE name=?", [clanTwoDefense, clanTwoVision, clanname])

        #clan 1
        clanOneAttack = clanOneAttack - 5
        clanOneGold = clanOneGold - 15 #looses 15 gold for battle reperations. (Winning gold pays for this therefor it is not factored in)

        c.execute("UPDATE kingdoms SET attack=?, gold=? WHERE owner=?", [clanOneAttack, clanOneGold, oname])

        #Commit db changes
        conn.commit()

        return "draw"

    elif clanOneAttack < clanTwoDefense:

        #clan 2
        clanTwoDefense = clanTwoDefense + 10
        clanTwoVision = clanTwoVision + 5
        clanTwoGold = clanTwoGold + 15

        c.execute("UPDATE kingdoms SET defense=?, vision=?, gold=? WHERE name=?", [clanTwoDefense, clanTwoVision, clanTwoGold, clanname])

        #clan 1
        clanOneAttack = clanOneAttack - 10
        clanOneVision = clanOneVision - 5
        clanOneGold = clanOneGold - 15

        c.execute("UPDATE kingdoms SET attack=?, vision=?, gold=? WHERE owner=?", [clanOneAttack, clanOneVision, clanOneGold, oname])

        conn.commit()

        return "{} has sucessfully defended against {}\'s raid!".format(clan, name)

    else:

        return "Something has happened here and I don\'t know what... ask Flaymed to look at the console... cause idk"
