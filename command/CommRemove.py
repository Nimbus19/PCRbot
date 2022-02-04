from misc.WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommRemove(BaseCommand):
    name="remove"
    help="Remove yourself from waiting queue.\n\n-remove\n-remove [boss number]\n-r\n-r [boss number]"
    brief="Remove yourself from waiting queue."
    aliases = ['r']
    slashSetting = {
        "name": name,
        "description": brief,
        "options": [
            {
                "name": "boss",
                "description": "The ID of boss",
                "type": 4,
                "required": False,
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
        async def remove(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _remove(ctx,  **args):            
            await self.execute(ctx, *(args.values()))


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        queue = self.getQueue(ctx.channel.id)
        userID = ctx.author.id

        if len(args) == 1:
            bossID = int(args[0]) - 1
            message = queue.delete(bossID, userID)
        else:
            for bossID in range(5):
                queue.delete(bossID, userID)
            message = '<@{}> is removed from **ALL**.'.format(userID)
            
        await ctx.send(content=message, delete_after=5)
        await ctx.message.delete(delay=5)

        