import json
import asyncio
import discord
import datetime
from discord.ext import commands
from os import path
from replit import db


waitlistDict = {}
nameDict = {}


def getWaitlist(channelID):
    if channelID in waitlistDict:
        return waitlistDict[channelID]         
    else:
        waitlistDict[channelID] = readWaitList(channelID)
        return waitlistDict[channelID]


def saveWaitList(channelID, waitlist):
    db[str(channelID)] = waitlist


def readWaitList(channelID):
    try:
        return db[str(channelID)]
    except KeyError:
        return {('1'):[], ('2'):[], ('3'):[], ('4'):[], ('5'):[]}
    

async def bossDead(ctx, arg):    
    waitlist = getWaitlist(ctx.channel.id)   
    userList = waitlist[str(int(arg) % 5 + 1)]
    users = ''
    if len(userList) > 0:
      users = '<@' + '><@'.join(userList) + '>'
    await ctx.channel.send('BOSS {} is dead'.format(arg))
    await ctx.channel.send('Ready to kill **BOSS {}** {}'.format((int(arg)) % 5 + 1, users))
    await asyncio.sleep(5)
    await ctx.message.delete()
    
   
async def waitBoss(ctx, arg):
    waitlist = getWaitlist(ctx.channel.id)
    author = str(ctx.message.author.id)
    nameDict[author] = ctx.message.author.name
    waitlist[arg].append(author)    
    message = await ctx.channel.send('<@{}> is waiting for **BOSS {}**.'.format(author, arg))
    saveWaitList(ctx.channel.id, waitlist)
    await asyncio.sleep(5)
    await ctx.message.delete()
    await message.delete()


async def showWaitList(ctx, *args):
    waitlist = getWaitlist(ctx.channel.id)
    messages = []
    if len(args) == 1:
        if len(waitlist[args[0]]) > 0:
            users = ''
            for uid in waitlist[args[0]]:
                users += getUserName(ctx, uid)
        else:
            users = 'Nobody '        
        messages.append(await ctx.channel.send('{}is waiting for **BOSS {}**.'.format(users, args[0])))
    elif len(args) == 0:
        for idx in waitlist:
            if len(waitlist[idx]) > 0:
                users = ''
                for uid in waitlist[idx]:
                  users += getUserName(ctx, uid)
            else:
                users = 'Nobody '
            messages.append(await ctx.channel.send('{}is waiting for **BOSS {}**.'.format(users, idx)))
    await asyncio.sleep(15)
    await ctx.message.delete()
    for message in messages:
        await message.delete()


async def removeSelf(ctx, *args):
    waitlist = getWaitlist(ctx.channel.id)
    author = str(ctx.message.author.id)
    if len(args) == 1:
        waitlist[args[0]] = list(filter(lambda x: x != author, waitlist[args[0]]))
        message = await ctx.channel.send('<@{}> is removed from waiting list of **BOSS {}**.'.format(author, args[0]))
    elif len(args) == 0:   
        for idx, boss in waitlist.items():
            waitlist[idx] = list(filter(lambda x: x != author, boss))
        message = await ctx.channel.send('<@{}> is removed from waiting list of **All BOSS**.'.format(author))
    saveWaitList(ctx.channel.id, waitlist)
    await asyncio.sleep(5)
    await ctx.message.delete()
    await message.delete()
    
async def clearDB(ctx, *args):
    if len(args) == 1:
        if args[0] == 'all':
            for channelID in list(db.keys()):
                del db[channelID] 
                await ctx.channel.send('delete {}'.format(channelID))
        else:
            del db[args[0]]
            await ctx.channel.send('delete {}'.format(args[0]))


def getUserName(ctx, uid):
  if uid in nameDict:
    return nameDict[uid] + '🧍 '

  user = ctx.bot.get_user(int(uid))

  # retry
  if user == None:
    user = ctx.bot.get_user(int(uid))
  
  if user == None:
    return '<@'+ uid + '>🧍 '
  else:
    nameDict[uid] = user.display_name
    return  user.display_name + '🧍 '