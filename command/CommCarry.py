from misc.WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommCarry(BaseCommand):
    name="carry"
    help="Announce you have a 持ち越し, you can cancel that by repeating this command."
    brief="Announce you have a 持ち越し."
    aliases = ['c']
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
        async def carry(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _carry(ctx,  **args):            
            await self.execute(ctx, *(args.values()))


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        queue = self.getQueue(ctx.channel.id)
        userID = ctx.author.id
        userName = ctx.author.display_name

        message = queue.carryOver(userID, userName)

        await ctx.send(content=message, delete_after=5)
        await ctx.message.delete(delay=5)

        