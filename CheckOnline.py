import asyncio
import discord 
import time

TIME = 300

async def checkOnline(message, bot, userForCheck):
    uID = userForCheck['ID']
    uName = userForCheck['Name']
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
        await asyncio.sleep(0.2)
        if time.time() - currentTime > 1:
            # Check if user press reaction
            if checkPass:
                break
            else:
                users = await accept_decline.reactions[0].users(limit=5).flatten()
                for user in users:
                    if user.id == uID:
                        checkPass = True
                        break

            # Update embed
            currentTime =  time.time()
            timer = int(currentTime - startTime)
            pannel.clear_fields()
            pannel.add_field(name = uName, value = 'Please press ⭕ in ' + str(max(TIME - timer, 0)) + ' s', inline = False)
            await accept_decline.edit(embed = pannel)           
        
        

    # Update Embaded
    pannel.clear_fields()
    if checkPass:                
        pannel.add_field(name = 'OK', value = '⭕')
    else:
        pannel.add_field(name = 'Fail', value = '❌')
    await accept_decline.edit(embed = pannel)    
    await accept_decline.clear_reactions()

    return checkPass

