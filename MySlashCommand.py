import requests


json = {
    "name": "show",
    "description": "顯示目前排隊狀況",
    "options": [
        # {
        #     "name": "boss ID",
        #     "description": "The ID of boss",
        #     "type": 4,
        #     "required": False,
        #     "choices": [
        #         {
        #             "name": "Boss 1",
        #             "value": 1
        #         },
        #         {
        #             "name": "Boss 2",
        #             "value": 2
        #         },
        #         {
        #             "name": "Boss 3",
        #             "value": 3
        #         },
        #         {
        #             "name": "Boss 4",
        #             "value": 4
        #         },
        #         {
        #             "name": "Boss 5",
        #             "value": 5
        #         }
        #     ]
        # }
     ]
}

def addSlashCommand(bot, token):
    headers = { "Authorization": "Bot " + token }   

    url = "https://discord.com/api/v8/applications/674909883195457577/guilds/626301417325461515/commands"    
    r:requests.Response = requests.post(url, headers=headers, json=json)
    print(r.status_code)
    print(r.text)

    # url = "https://discord.com/api/v8/applications/674909883195457577/guilds/626301417325461515/commands/859061730687713280"
    # r:requests.Response = requests.delete(url, headers=headers)    
    # print(r.status_code)
    # print(r.text)

    url = "https://discord.com/api/v8/applications/674909883195457577/guilds/626301417325461515/commands"
    r:requests.Response = requests.get(url, headers=headers)    
    print(r.status_code)
    print(r.text)

   
    
