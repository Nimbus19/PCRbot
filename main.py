import json as JSON
import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import keep_alive

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
    APP_ID = config['APP_ID']
    ADMIN_UID = config['ADMIN_UID']

# Create bot object of discord
bot = commands.Bot(command_prefix = CMD_PREFIX, intents=discord.Intents.all())
slash = SlashCommand(bot)
guildID = 626301417325461515

# --------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    if message.content.startswith(CMD_PREFIX):
        print(message.author.display_name + ' : ' + message.content )
        await bot.process_commands(message)

@bot.event
async def on_slash_command(ctx: SlashContext):
    options = str(ctx.data['options'])  if 'options' in ctx.data else ''
    print(ctx.author.display_name + ' : / ' + ctx.command + ' ' + options)
        
# --------------------------------------------------------------------------------------------------
from command.CommShow import CommShow
comm = CommShow(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommWait import CommWait
comm = CommWait(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommRemove import CommRemove
comm = CommRemove(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommDead import CommDead
comm = CommDead(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommCarry import CommCarry
comm = CommCarry(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommNeed import CommNeed
comm = CommNeed(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener()

from command.CommClear import CommClear
comm = CommClear(bot, slash, DISCORD_TOKEN, APP_ID, guildID)
comm.addListener(ADMIN_UID)

# --------------------------------------------------------------------------------------------------
@bot.command(
    hidden = True,
    aliases = ['q']
)
async def query(ctx, arg):
    print(arg)

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