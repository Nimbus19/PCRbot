from misc.WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommNeed(BaseCommand):
    name="need"
    help="Announce you need a 持ち越し."
    brief="Announce you need a 持ち越し."
    aliases = ['n']
    slashSetting = {
        "name": name,
        "description": brief
    }

    def addListener(self):
        @self.bot.command(
            name = self.name,
            help = self.help,
            brief = self.brief,
            aliases = self.aliases
        )
        async def need(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _need(ctx,  **args):            
            await self.execute(ctx, *(args.values()))


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        queue = self.getQueue(ctx.channel.id)
        message = queue.needCarry()
        await ctx.send(content=message)

        