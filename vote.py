import asyncio
import discord 


async def voteToBurn(message, bot):
    channel = bot.get_channel(message.channel.id)
    #accept_decline = await channel.send('🔥投票燒人 {0.mentions[0].mention}🔥'.format(message))  
    
    vote = discord.Embed(title = '🔥**投票燒 {0.mentions[0].name}**🔥'.format(message), description = '', color = 0x00ff00)
    vote.add_field(name = '請在2分鐘內進行投票', value = '120秒')
    accept_decline = await channel.send(embed = vote)  
    
    # Add emoji to message
    for emoji in ('👍', '👎'):
        await accept_decline.add_reaction(emoji)

    # Timer
    for timer in range(0, 120):
        vote.clear_fields()
        vote.add_field(name = '請在2分鐘內進行投票', value = str(120 - timer) + '秒')
        await accept_decline.edit(embed = vote)
        await asyncio.sleep(1)

    # Count reactions
    accept_decline = await channel.fetch_message(accept_decline.id)
    upvote = accept_decline.reactions[0].count - 1
    downvote = accept_decline.reactions[1].count - 1

    # Update Embaded
    vote.clear_fields()
    if upvote - downvote > 0:                
        vote.add_field(name = "投票結果", value = '{0.mentions[0].mention} 已經被燒掉了 ('.format(message) + str(upvote) + '-' + str(downvote) + ')')
    elif upvote - downvote < 0:
        vote.add_field(name = "投票結果", value = '{0.mentions[0].mention} 已經被解鎖了 ('.format(message) + str(upvote) + '-' + str(downvote) + ')')
    elif upvote + downvote == 0:
        vote.add_field(name = "投票結果", value = '{0.mentions[0].mention} 沒人理你，可憐哪 ('.format(message) + str(upvote) + '-' + str(downvote) + ')')
    else:
        vote.add_field(name = "投票結果", value = '毫無反應 (' + str(upvote) + '-' + str(downvote) + ')')
    await accept_decline.edit(embed = vote)    
    await accept_decline.clear_reactions()    
                  

