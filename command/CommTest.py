from misc.WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommTest(BaseCommand):
    name = "test"
    brief="Test brief"
    help="Test help message"
    aliases = ['t']
    slashSetting = {
        "name": name,
        "description": brief,
    }

    def addListener(self):
        @self.bot.command(
            name = self.name,
            help = self.help,
            brief = self.brief,
            aliases = self.aliases
        )
        async def test(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _test(ctx,  **args):            
            await self.execute(ctx, *(args.values()))  


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):
        queue = self.getQueue(ctx.channel.id)     

        if len(args) == 1:
            message = queue.show(int(args[0]) - 1)
        else:
            message = queue.showAll()

        await ctx.send(content=message, delete_after=15)
        await ctx.message.delete(delay=15)

