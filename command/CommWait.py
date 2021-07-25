from WaitQueues import WaitQueues
from command.BaseCommand import BaseCommand


class CommWait(BaseCommand):
    name="wait"
    help="Tell bot you are waiting for this boss, the bot will remind you when privous one is dead.\n\n-wait [boss number]\n-w [boss number]"
    brief="Add yourself into waiting queue."
    aliases = ['w']
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
            },
            {
                "name": "damage",
                "description": "Expected damage",
                "type": 4,
                "required": False
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
        async def wait(ctx, *args):
            await self.execute(ctx, *args)

        @self.slash.slash(name = self.name)
        async def _wait(ctx,  **args):            
            await self.execute(ctx, *(args.values()))


    def getQueue(self, channelID):    
        varPool = self.getSharedVar()
        if channelID not in varPool:
            varPool[channelID] = WaitQueues(channelID)
        return varPool[channelID]


    async def execute(self, ctx, *args):   
        bossID = int(args[0]) - 1
        if bossID in range(5):            
            userID = ctx.author.id
            userName = ctx.author.display_name
            damage = args[1] if len(args) > 1 else 'None'
            queue = self.getQueue(ctx.channel.id)
            message = queue.add(bossID, userID, userName, damage)

            await ctx.send(content=message, delete_after=5)
            await ctx.message.delete(delay=5)

        