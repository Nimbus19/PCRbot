import json
import requests
from discord.ext import commands
from discord_slash import SlashCommand

# Shared variables between commands
sharedVariables = dict()

# --------------------------------------------------------------------------------------------------
class BaseCommand(): 
    name: str
    apiURL: str = "https://discord.com/api/v8"


    def __init__(
        self, 
        bot: commands.Bot, 
        slash: SlashCommand,
        token: str,
        appId: int,
        guildID: int = 0,
    ):
        self.bot = bot
        self.slash = slash
        self.token = token
        self.headers = { "Authorization": "Bot " + token }
        self.appId = appId
        self.guildID = guildID
        self.apiURL += "/applications/" + str(appId)
        if guildID != 0:
            self.apiURL += "/guilds/" + str(guildID)  

        
            
    def registerSlashCommand(self, slashSetting):
        self.commandID = self.getSlashCommandID()
        if self.commandID == None:            
            self.commandID = self.addSlashCommand(self.slashSetting)           
        else :
            self.updateSlashCommand(self.slashSetting)

    def addSlashCommand(self, slashSetting):        
        url = self.apiURL + "/commands"   
        r:requests.Response = requests.post(url, headers=self.headers, json=slashSetting)
        response = json.loads(r.text)
        print( "Add Slash Command '" + self.name + "' response : " + str(r.status_code))
        return response['id']


    def updateSlashCommand(self, slashSetting):
        self.commandID = self.getSlashCommandID()        
        url = self.apiURL + "/commands/" + str(self.commandID)
        r:requests.Response = requests.patch(url, headers=self.headers, json=slashSetting)
        response = json.loads(r.text)
        print( "Update Slash Command '" + self.name + "' response : " + str(r.status_code))
        return response['id']


    def deleteSlashCommand(self):
        self.commandID = self.getSlashCommandID()        
        url = self.apiURL + "/commands/" + str(self.commandID)
        r:requests.Response = requests.delete(url, headers=self.headers)
        print( "Delete Slash Command '" + self.name + "' response : " + str(r.status_code))


    def getSlashCommandID(self):
        url = self.apiURL + "/commands"  
        r:requests.Response = requests.get(url, headers=self.headers)
        response = json.loads(r.text)
        for command in response:
            if command['name'] == self.name:
                return command['id']
        return None


    def getSharedVar(self):
        return sharedVariables

