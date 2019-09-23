#import modules
import dbmanager
import time
import sqlite3
import discord
from discord.ext import commands

conn = sqlite3.connect('./database/main.db')
c = conn.cursor()

bot = commands.Bot(command_prefix='!', description='A bot that does some cool stuff!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    dbmanager.onReady()

@bot.event
async def on_message(ctx):
    ctx.content = ctx.content.lower()
    await bot.process_commands(ctx)

#example of checking for argument being passed.
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

#stop command
@bot.command()
async def stop(ctx):
    if ctx.author.id == 259441701427347456:
        await ctx.send('Stopping the bot.')
        await bot.logout()
    else:
        await ctx.send('Sorry, only Flaymed can do this command.')

bot.run('your token here')
