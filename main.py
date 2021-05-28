import os
import json
import asyncio
import discord
import gvg
import vote
import keep_alive
from discord.ext import commands
from replit import db


with open('config.json','r', encoding="utf8") as f:
    config = json.load(f)
    CMD_PREFIX = config['CMD_PREFIX']
    DISCORD_TOKEN = config['DISCORD_TOKEN']
    channel_list = [config['BOSS1_CHANNEL'], config['BOSS2_CHANNEL'], config['BOSS3_CHANNEL'], config['BOSS4_CHANNEL'], config['BOSS5_CHANNEL']]
    search_url_list = [config['BOSS1_SEARCH'], config['BOSS2_SEARCH'], config['BOSS3_SEARCH'], config['BOSS4_SEARCH'], config['BOSS5_SEARCH']]
    default_url = config['YOUTUBE']

alredy_href_list = [[],[],[],[],[]]

# Create bot object of discord
bot = commands.Bot(command_prefix = CMD_PREFIX)

@bot.event
async def on_message(message):
    if message.content.startswith('-'):
        print(message.author.display_name + ' : ' + message.content )
        await bot.process_commands(message)


         
@bot.command(
    pass_context = True,
    help="Report this boss is dead, and notify people who is waiting for next.\n\n-dead [boss number] \n-d [boss number]",
    brief="Report this boss is dead.",
    aliases = ['d']
)
async def dead(ctx, arg):
    await gvg.bossDead(ctx, arg)

@bot.command(
    pass_context = True,
    help="Tell bot you are waiting for this boss, the bot will remind you when privous one is dead.\n\n-wait [boss number]\n-w [boss number]",
    brief="Add yourself into waiting queue.",
    aliases = ['w']
)
async def wait(ctx, arg):
    await gvg.waitBoss(ctx, arg)

@bot.command(
    pass_context = True,
    help="Show waiting queue of each boss\n\n-show\n-show [boss number]\n-s\n-s [boss number]",
    brief="Show waiting queue.",
    aliases = ['s']
)
async def show(ctx, *args):
    await gvg.showWaitList(ctx, *args)

@bot.command(
    pass_context = True,
    help="Remove yourself from waiting queue.\n\n-remove\n-remove [boss number]\n-r\n-r [boss number]",
    brief="Remove yourself from waiting queue.",
    aliases = ['r']
)
async def remove(ctx, *args):
    await gvg.removeSelf(ctx, *args)

@bot.command(
    hidden = True
)
async def clearDB(ctx, *args):
    await gvg.clearDB(ctx, *args)

@bot.command(
    pass_context = True,
    help="-burn [被燒者mention] : 燒人",
    brief="Vote to burn(for fun).",
    aliases = ['b']
)
async def burn(ctx):
    await vote.voteToBurn(ctx.message, ctx.bot)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for channelID in list(db.keys()):
      print(channelID)
      print(db[channelID])
    await bot.change_presence(activity=discord.Game(name="-help"))

keep_alive.keep_alive()
bot.run(DISCORD_TOKEN)