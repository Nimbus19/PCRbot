import re
import asyncio
import discord
from CheckOnline import *
from WaitQueues import WaitQueues

# Global variables
waitQueues = {}

def initWaitQueue(channelID):
    if channelID not in waitQueues:
        waitQueues[channelID] = WaitQueues(channelID)

# --------------------------------------------------------------------------------------------------
async def waitBoss(ctx, arg):
    bossID = int(arg) - 1
    if bossID in range(5):
        waitQueue = waitQueues[ctx.channel.id]
        message = waitQueue.add(bossID, ctx.message.author.id, ctx.message.author.display_name)
        await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
async def bossDead(ctx, arg):
    waitQueue = waitQueues[ctx.channel.id]
    bossID = int(arg) - 1
    if bossID in range(5):
        messageAndUser = waitQueue.notifyNext(bossID)
        message = messageAndUser[0]
        userForCheck = messageAndUser[1]
        await sendMessage(ctx, message)
        if userForCheck != None:
            response = await checkOnline(ctx.message, ctx.bot, userForCheck)
            if response == False:
                message2 = waitQueue.add(6, userForCheck[0], userForCheck[1])
                await sendMessage(ctx, message2, 5)

# --------------------------------------------------------------------------------------------------
async def showQueue(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    if len(args) == 1:
        message = queue.show(int(args[0]) - 1)
    else:
        message = queue.showAll()
    await sendMessage(ctx, message, 15)

# --------------------------------------------------------------------------------------------------
async def removeFromQueue(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    if len(args) == 1:
        bossID = int(args[0]) - 1
        message = queue.delete(bossID, ctx.message.author.id, ctx.message.author.display_name)
    else:
        for bossID in range(5):
            queue.delete(bossID, ctx.message.author.id, ctx.message.author.display_name)
        message = '<@{}> is removed from **ALL**.'.format(ctx.message.author.id)
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
async def sendMessage(ctx, message, deleteMessageInSecond = None):
    command = ctx.message
    handle = await ctx.channel.send(message)
    if deleteMessageInSecond != None:
        await asyncio.sleep(deleteMessageInSecond)        
        await handle.delete()
        try:
            await command.delete()            
        except:
            print('Error : 404 Not Found')

# --------------------------------------------------------------------------------------------------
async def addCarryOver(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    message = queue.carryOver(ctx.message.author.id, ctx.message.author.display_name)
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
async def needCarryOver(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    message = queue.needCarry()
    await sendMessage(ctx, message)

# --------------------------------------------------------------------------------------------------
async def queryUID(ctx, arg):
    message = arg + '\'s UID is ' + re.search('[\d]+', arg).group()
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
async def clearQueue(ctx, arg):
    queue = waitQueues[ctx.channel.id]
    if  arg == 'all':
        message = queue.clearAll()
    elif arg[0] == '<':
        message = queue.clearUser(int(re.search('[\d]+', arg).group()))
    elif int(arg) <= len(queue.nameList):
        message = queue.clearQueue(int(arg) - 1)
    await sendMessage(ctx, message, 5)
