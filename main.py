import json as JSON
import asyncio
import discord
from discord.ext import commands
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import keep_alive
from MyCommand import *
from MySlashCommand import *

try:
    from replit import db
    replit_db = True
except ImportError:
    replit_db = False

# main start
with open('config.json','r', encoding="utf8") as f:
    config = JSON.load(f)
    CMD_PREFIX = config['CMD_PREFIX']
    DISCORD_TOKEN = config['DISCORD_TOKEN']
    ADMIN_UID = config['ADMIN_UID']

# Create bot object of discord
bot = commands.Bot(command_prefix = CMD_PREFIX, intents=discord.Intents.all())
slash = SlashCommand(bot)

# Global variables
activeChannel = []

# --------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    if message.content.startswith(CMD_PREFIX):

        if message.channel.id not in activeChannel:
            initWaitQueue(message.channel.id)
            activeChannel.append(message.channel.id)

        print(message.author.display_name + ' : ' + message.content )
        await bot.process_commands(message)

# --------------------------------------------------------------------------------------------------
@bot.command(
    name="wait",
    help="Tell bot you are waiting for this boss, the bot will remind you when privous one is dead.\n\n-wait [boss number]\n-w [boss number]",
    brief="Add yourself into waiting queue.",
    aliases = ['w']
)
async def wait(ctx, arg):
    await waitBoss(ctx, arg)

@slash.slash(name="wait")
async def _wait(ctx: SlashContext):
    await ctx.send(content=ctx.author.display_name+":/wait", delete_after=5)
    await waitBoss(ctx, ctx.args[0])

 # --------------------------------------------------------------------------------------------------        
@bot.command(
    name="dead",
    help="Report this boss is dead, and notify people who is waiting for next.\n\n-dead [boss number] \n-d [boss number]",
    brief="Report this boss is dead.",
    aliases = ['d']
)
async def dead(ctx, arg):
    await bossDead(ctx, arg)

@slash.slash(name="dead")
async def _dead(ctx: SlashContext):
    await ctx.send(content=ctx.author.display_name+":/dead", delete_after=5)
    await bossDead(ctx, ctx.args[0])

# --------------------------------------------------------------------------------------------------
@bot.command(
    name="show",
    help="Show waiting queue of each boss\n\n-show\n-show [boss number]\n-s\n-s [boss number]",
    brief="Show waiting queue.",
    aliases = ['s']
)
async def show(ctx, *args):
    await showQueue(ctx, *args)

@slash.slash(name="show")
async def _show(ctx: SlashContext):
    await ctx.send(content=ctx.author.display_name+":/show", delete_after=15)    
    await showQueue(ctx, *(ctx.args))

# --------------------------------------------------------------------------------------------------
@bot.command(
    name="remove",
    help="Remove yourself from waiting queue.\n\n-remove\n-remove [boss number]\n-r\n-r [boss number]",
    brief="Remove yourself from waiting queue.",
    aliases = ['r']
)
async def remove(ctx, *args):
    await removeFromQueue(ctx, *args)

# --------------------------------------------------------------------------------------------------
@bot.command(
    name="carry",
    help="Announce you have a 持ち越し, you can cancel that by repeating this command.",
    brief="Announce you have a 持ち越し.",
    aliases = ['c']
)
async def carry(ctx, *args):
    await addCarryOver(ctx, *args)

# --------------------------------------------------------------------------------------------------
@bot.command(
    name="need",
    help="Announce you need a 持ち越し.",
    brief="Announce you need a 持ち越し.",
    aliases = ['n']
)
async def need(ctx, *args):
    await needCarryOver(ctx, *args)

# --------------------------------------------------------------------------------------------------
@bot.command(
    hidden = True,
    aliases = ['q']
)
async def query(ctx, arg):
    await queryUID(ctx, arg)

# --------------------------------------------------------------------------------------------------
@bot.command(
    hidden = True
)
async def clear(ctx, arg):
    if (ctx.message.author.id) in ADMIN_UID:
        await clearQueue(ctx, arg)
    else:
        message = 'You need admin privileges.'
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
addSlashCommand(bot, DISCORD_TOKEN)
bot.run(DISCORD_TOKEN)