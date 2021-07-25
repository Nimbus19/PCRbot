import re
from WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommClear(BaseCommand):
    name="clear"
    hidden = True

    def addListener(self, whiteList):
        self.whiteList = whiteList

        @self.bot.command(
            name = self.name,
            hidden = True
        )
        async def carry(ctx, *args):
            await self.execute(ctx, *args)
            

    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        queue = self.getQueue(ctx.channel.id)
        userID = ctx.author.id

        if userID in self.whiteList:
            if args[0] == 'all':
                message = queue.clearAll()
            elif args[0][0] == '<':
                message = queue.clearUser(int(re.search('[\d]+', args[0]).group()))
            elif int(args[0]) <= len(queue.queuesName):
                message = queue.clearQueue(int(args[0]) - 1)
        else:
            message = 'You need admin privileges.'

        await ctx.send(content=message, delete_after=5)
        await ctx.message.delete(delay=5)

