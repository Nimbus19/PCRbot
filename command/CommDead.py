from misc.WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand
from misc.CheckOnline import *

class CommDead(BaseCommand):
    name="dead"
    help="Report this boss is dead, and notify people who is waiting for next.\n\n-dead [boss number] \n-d [boss number]"
    brief="Report this boss is dead."
    aliases = ['d']
    slashSetting = {
        "name": name,
        "description": brief,
        "options": [
            {
                "name": "boss",
                "description": "The ID of boss",
                "type": 4,
                "required": True,
                "choices": [
                    {
                        "name": "Boss 1",
                        "value": 1
                    },
                    {
                        "name": "Boss 2",
                        "value": 2
                    },
                    {
                        "name": "Boss 3",
                        "value": 3
                    },
                    {
                        "name": "Boss 4",
                        "value": 4
                    },
                    {
                        "name": "Boss 5",
                        "value": 5
                    }
                ]
            }
        ]
    }

    def addListener(self):
        @self.bot.command(
            name = self.name,
            help = self.help,
            brief = self.brief,
            aliases = self.aliases
        )
        async def dead(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _dead(ctx,  **args):            
            await self.execute(ctx, *(args.values()))


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        queue = self.getQueue(ctx.channel.id)    
        bossID = int(args[0]) - 1

        if bossID in range(5):
            messageAndUser = queue.notifyNext(bossID)
            message = messageAndUser[0]
            userForCheck = messageAndUser[1]
            await ctx.send(content=message)
            if userForCheck != None:
                response = await checkOnline(ctx.message, ctx.bot, userForCheck)
                if response == False:
                    message2 = queue.add(6, userForCheck['ID'], userForCheck['Name'])
                    await ctx.send(content=message2, delete_after=5)
                         

        