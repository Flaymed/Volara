#import modules
import dbmanager
import ally
import raid
import time
import sqlite3
import discord
from discord.ext import commands

conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

bot = commands.Bot(command_prefix='!', description='A bot that does some cool stuff!')

#event handling

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    dbmanager.onReady()

@bot.event
async def on_message(ctx):
    ctx.content = ctx.content.lower()
    await bot.process_commands(ctx)

#Kingdom management

@bot.command()
async def createkingdom(ctx, name = None):
    ownerid = ctx.author.id
    if name:
        if dbmanager.checkOwner(ownerid) == False:
            if dbmanager.checkExist(name) == False:
                dbmanager.createKingdom(name, ctx.author.name ,ctx.author.id)
                await ctx.send('{} has created a kingdom named: {}'.format(ctx.author.name, name))
            else:
                await ctx.send('It appears a clan with that name already exists!')
        else:
            await ctx.send('Sorry dude you already own a kingdom!')
    else:
        await ctx.send('Please provide a name!')

@bot.command()
async def deletekingdom(ctx, name = None):
    id = ctx.author.id
    if name:
        if dbmanager.checkExist(name):
            if dbmanager.checkKingdomOwner(name, id):
                dbmanager.deleteKingdom(name)
                await ctx.send('Kingdom deleted, you may now create a new kingdom!')
            else:
                await ctx.send('You must own the kingdom you wish to delete!')
        else:
            await ctx.send('It appears the kingdom you provided does not exist!')
    else:
        await ctx.send('Please provide a kingdom to delete!')

#Gold top

@bot.command()
async def goldtop(ctx):
    teams = dbmanager.goldTopName()
    gold = dbmanager.goldTop()
    i = 0
    embed = discord.Embed(title="Gold Top", description="Rankings based on gold count of a kingdom.", color=0x00ff00)
    while i < len(teams):
        embed.add_field(name="{}. {}".format(i + 1, teams[i]), value=gold[i], inline=False)
        i += 1
    await ctx.send(embed=embed)

#Mining

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def mine(ctx):
    id = ctx.author.id
    if dbmanager.ownsKingdom(id):
        await ctx.send('You\'ve sent a mining crew out to mine for gold!')
        gold = dbmanager.mine()
        time.sleep(4)
        dbmanager.addGold(id, gold)
        await ctx.send('Your miners found {} pieces of gold!'.format(gold))
    else:
        await ctx.send('You must own a kingdom before you can go mining!')

#Raid system

@bot.command()
@commands.cooldown(1, 90, commands.BucketType.user)
async def raid(ctx, clantoraid = None):
    id = ctx.author.id
    if clantoraid:
        if dbmanager.checkExist(clantoraid):
            if dbmanager.checkOwner(id):
                if ally.checkAlly(id, clantoraid):
                    await ctx.message.guild.get_member(dbmanager.getKingdomOwnerId(clantoraid)).send("Your ally as attempted to raid you!")
                    await ctx.send('You cannot raid an ally! I have notified your ally that you tried to raid them!')
                else:
                    await ctx.send(raid.startRaid(id, clantoraid))
            else:
                await ctx.send('You must own a kingdom to raid another kingdom!')
        else:
            await ctx.send('It appears the kingdom you are trying to raid does not exist!')
    else:
        await ctx.send('Please supply a kingdom you wish to raid!')

#Allying System

@bot.command()
async def requests(ctx):
    id = ctx.author.id
    if dbmanager.checkOwner(id):
        request = ally.isRequested(id)
        if not request:
            await ctx.send("No requests")
        else:
            await ctx.send(request)
    else:
        await ctx.send('You must own a kingdom before you can perform this action!')

@bot.command()
async def unally(ctx, clanname = None):
    id = ctx.author.id
    if clanname:
        if dbmanager.checkOwner(id):
            if dbmanager.checkExist(clanname):
                if ally.checkAlly(id, clanname):
                    await ctx.send(ally.removeAlly(id, clanname))
                else:
                    await ctx.send('You must be allied with {} to unally them!'.format(clanname))
            else:
                await ctx.send('It appears the clan you wish to unally does not exist!')
        else:
            await ctx.send('You must own a kingdom before performing this action!')
    else:
        await ctx.send('Provide a clan to unally!')

#stop command
@bot.command()
async def stop(ctx):
    if ctx.author.id == 259441701427347456:
        await ctx.send('Stopping the bot.')
        await bot.logout()
    else:
        await ctx.send('Sorry, only Flaymed can do this command.')

bot.run('your token here')
