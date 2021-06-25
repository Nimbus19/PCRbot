import json
import asyncio
import discord
import keep_alive
from WaitQueues import WaitQueues
from CheckOnline import checkOnline
from discord.ext import commands

try:
    from replit import db
    replit_db = True
except ImportError:
    replit_db = False

# main start
with open('config.json','r', encoding="utf8") as f:
    config = json.load(f)
    CMD_PREFIX = config['CMD_PREFIX']
    DISCORD_TOKEN = config['DISCORD_TOKEN']
    ADMIN_UID = config['ADMIN_UID']

# Create bot object of discord
bot = commands.Bot(command_prefix = CMD_PREFIX)

# Global variables
waitQueues = {}

# --------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    if message.content.startswith('-'):
        # Create queue object for each channel of discord
        if message.channel.id not in waitQueues:
            waitQueues[message.channel.id] = WaitQueues(message.channel.id)

        print(message.author.display_name + ' : ' + message.content )
        await bot.process_commands(message)

# --------------------------------------------------------------------------------------------------
@bot.command(
    help="Tell bot you are waiting for this boss, the bot will remind you when privous one is dead.\n\n-wait [boss number]\n-w [boss number]",
    brief="Add yourself into waiting queue.",
    aliases = ['w']
)
async def wait(ctx, arg):
    bossID = int(arg) - 1
    if bossID in range(5):
        waitQueue = waitQueues[ctx.channel.id]
        message = waitQueue.add(bossID, ctx.message.author.id, ctx.message.author.display_name)
        await sendMessage(ctx, message, 5)

 # --------------------------------------------------------------------------------------------------        
@bot.command(
    help="Report this boss is dead, and notify people who is waiting for next.\n\n-dead [boss number] \n-d [boss number]",
    brief="Report this boss is dead.",
    aliases = ['d']
)
async def dead(ctx, arg):
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
@bot.command(
    help="Show waiting queue of each boss\n\n-show\n-show [boss number]\n-s\n-s [boss number]",
    brief="Show waiting queue.",
    aliases = ['s']
)
async def show(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    if len(args) == 1:
        message = queue.show(int(args[0]) - 1)
    else:
        message = queue.showAll()
    await sendMessage(ctx, message, 15)

# --------------------------------------------------------------------------------------------------
@bot.command(
    help="Remove yourself from waiting queue.\n\n-remove\n-remove [boss number]\n-r\n-r [boss number]",
    brief="Remove yourself from waiting queue.",
    aliases = ['r']
)
async def remove(ctx, *args):
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
@bot.command(
    help="Announce you have a 持ち越し, you can cancel that by repeating this command.",
    brief="Announce you have a 持ち越し.",
    aliases = ['c']
)
async def carry(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    message = queue.carryOver(ctx.message.author.id, ctx.message.author.display_name)
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
@bot.command(
    help="Announce you need a 持ち越し.",
    brief="Announce you need a 持ち越し.",
    aliases = ['n']
)
async def need(ctx, *args):
    queue = waitQueues[ctx.channel.id]
    message = queue.needCarry()
    await sendMessage(ctx, message)

# --------------------------------------------------------------------------------------------------
@bot.command(
    hidden = True,
    aliases = ['q']
)
async def query(ctx, arg):
    message = arg + '\'s UID is ' + arg[3:len(arg)-1]
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
@bot.command(
    hidden = True
)
async def clear(ctx, arg):
    queue = waitQueues[ctx.channel.id]
    if ctx.message.author.id in ADMIN_UID:
        if  arg == 'all':
            message = queue.clearAll()
        elif arg[0] == '<':
            message = queue.clearUser(int(arg[3:len(arg)-1]))
        elif int(arg) <= len(queue.nameList):
            message = queue.clearQueue(int(arg) - 1)
    else:
        message = 'You need admin privileges.'
    await sendMessage(ctx, message, 5)

# --------------------------------------------------------------------------------------------------
async def sendMessage(ctx, message, deleteMessageInSecond = None):
    handle = await ctx.channel.send(message)
    if deleteMessageInSecond != None:
        await asyncio.sleep(deleteMessageInSecond)
        await ctx.message.delete()
        await handle.delete()
        
# --------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="-help"))

# --------------------------------------------------------------------------------------------------
if replit_db:
    keep_alive.keep_alive()
bot.run(DISCORD_TOKEN)