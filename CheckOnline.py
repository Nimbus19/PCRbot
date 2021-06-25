import asyncio
import discord 
import time

TIME = 300

async def checkOnline(message, bot, userForCheck):
    uID = userForCheck[0]
    uName = userForCheck[1]
    channel = bot.get_channel(message.channel.id)
    
    pannel = discord.Embed(title = '🔥**Online Check for {}**🔥'.format(uName), description = '', color = 0x00ff00)
    pannel.add_field(name = uName , value =  'Please press ⭕ in '+ str(TIME) +' s')
    accept_decline = await channel.send(embed = pannel)  
    
    # Add emoji to message
    await accept_decline.add_reaction('⭕')
    accept_decline = await channel.fetch_message(accept_decline.id)

    # Timer
    checkPass = False
    startTime =  time.time()
    currentTime =  startTime
    while currentTime - startTime < TIME:
        await asyncio.sleep(5)
        currentTime =  time.time()
        timer = int(currentTime - startTime)

        # Update embed
        pannel.clear_fields()
        pannel.add_field(name = uName, value = 'Please press ⭕ in ' + str(max(TIME - timer, 0)) + ' s', inline = False)
        await accept_decline.edit(embed = pannel)

        # Check if user press reaction
        if checkPass:
            break
        else:
            async for user in accept_decline.reactions[0].users():
                if user.id == uID:
                    checkPass = True
                    break
        
        

    # Update Embaded
    pannel.clear_fields()
    if checkPass:                
        pannel.add_field(name = 'OK', value = '⭕')
    else:
        pannel.add_field(name = 'Fail', value = '❌')
    await accept_decline.edit(embed = pannel)    
    await accept_decline.clear_reactions()

    return checkPass

