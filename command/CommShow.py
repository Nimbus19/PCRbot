from WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommShow(BaseCommand):
    name="show"
    help="Show waiting queue of each boss\n\n-show\n-show [boss number]\n-s\n-s [boss number]"
    brief="Show waiting queue."
    aliases = ['s']
    slashSetting = {
        "name": name,
        "description": brief,
        "options": [
            {
                "name": "queue",
                "description": "The name of queue",
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
                    },
                    {
                        "name": "持ち越し",
                        "value": 6
                    },
                    {
                        "name": "叫號未到",
                        "value": 7
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
        async def show(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _show(ctx,  **args):            
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