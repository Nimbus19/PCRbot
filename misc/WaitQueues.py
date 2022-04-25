import sys
import json
from datetime import datetime
try:
    from replit import db
    replit_db = True
except ImportError:
    replit_db = False

dateFormat = "%m/%d %H:%M:%S"
class UserData(dict):    
    def __init__(self, id = 0, name = "", damage = "", timestamp = ""):
        self["ID"] = id
        self["Name"] = name
        self["Damage"] = damage
        self["Timestamp"] = timestamp


class WaitQueues:
    queuesName = ["Boss 1", "Boss 2", "Boss 3", "Boss 4", "Boss 5", "持ち越し", "叫號未到"]

# --------------------------------------------------------------------------------------------------
    def __init__(self, channelID):
        self.channelID = str(channelID)
        self.__load__()

# --------------------------------------------------------------------------------------------------
    def __load__(self):
        if (replit_db):
            try:
                self.queues = db[self.channelID]
            except KeyError:
                self.queues = {i : [] for i in self.queuesName}
        else:
            try:
                with open(self.channelID + ".json", "r", encoding="UTF-8") as file:
                    jsDict = json.load(file)
                self.queues = {i : jsDict[i] for i in self.queuesName}
            except:
                self.queues = {i : [] for i in self.queuesName}

# --------------------------------------------------------------------------------------------------
    def __save__(self):
        if (replit_db):
            db[self.channelID] = self.queues
        else:
            with open(self.channelID + ".json", "w", encoding="UTF-8") as file: 
                json.dump(self.queues, file, indent=4, ensure_ascii= False)

# --------------------------------------------------------------------------------------------------
    def __gettUsers__(self, queueIdx, number = sys.maxsize):
        key = self.queuesName[queueIdx]
        users = []
        for i in self.queues[key]:
            users.append(i)
            number = number - 1
            if number == 0:
                break
        return users


# --------------------------------------------------------------------------------------------------
    def add(self, queueIdx, userID, userName, damage = "None"):
        key = self.queuesName[queueIdx]
        newUser = UserData(userID, userName,  damage, datetime.now().strftime(dateFormat))
        self.queues[key].append(newUser)
        self.__save__()
        return "<@{}> is add to queue of **{}**".format(userID, key)

# --------------------------------------------------------------------------------------------------
    def delete(self, queueIdx, ID):
        key = self.queuesName[queueIdx]
        self.queues[key] = [i for i in self.queues[key] if i["ID"] != ID]
        self.__save__()
        return "<@{}> is removed from **{}**".format(ID, key)

# --------------------------------------------------------------------------------------------------
    def show(self, queueIdx):
        key = self.queuesName[queueIdx]
        users = self.__gettUsers__(queueIdx)
        userString = str(key) + ": \n"
        if len(users) > 0:
            for i, user in enumerate(users):
                userString += str(i + 1) + ". " + user["Name"]
                userString += "`(" + user["Timestamp"] + ")` "
                if user["Damage"] != "None":
                    userString += " `預期傷害:" + user["Damage"] + "` " 
                userString += "\n"
        else:
            userString = "Nobody "
        return userString

# --------------------------------------------------------------------------------------------------
    def showAll(self):
        message = ""
        for i in range(len(self.queuesName)):
            key = self.queuesName[i]
            users = self.__gettUsers__(i)
            userString = ""
            if len(users) > 0:
                for user in users:
                    userString += user["Name"] + "🧍 "
            else:
                userString = "Nobody "
            message += "**{}**: {}\n".format(key, userString)
        return message

# --------------------------------------------------------------------------------------------------
    def notifyNext(self, queueIdx):
        message = ""

        # Notify next one in the queue
        users = self.__gettUsers__(queueIdx, 1)
        if len(users) > 0:
            message += "Are you ready to hit **{}**? -> ".format(self.queuesName[queueIdx])
            for i in users:
                message += "<@{}>".format(i["ID"])
            message += "\n"
            hightest = users[0]
        else:
            message += "Nobody is waiting for **{}**\n".format(self.queuesName[queueIdx])
            hightest = None        

        return [message, hightest]

# --------------------------------------------------------------------------------------------------
    def carryOver(self, ID, Name):
        key = self.queuesName[5]
        queue = self.queues[key]

        for user in queue:
            if user['ID'] == ID:
                return self.delete(5, ID) 

        return self.add(5, ID, Name)

# --------------------------------------------------------------------------------------------------
    def needCarry(self):
        key = self.queuesName[5]
        if len(self.queues[key]) > 0:
            message = "Someone need 持ち越し "
            for i in self.queues[key]:
                message += "<@{}> ".format(i["ID"])
        else:
            message = "No one has 持ち越し"
        return message

# --------------------------------------------------------------------------------------------------
    def clearUser(self, ID):
        for key in self.queuesName:
            self.queues[key] = [i for i in self.queues[key] if i["ID"] != ID]
        self.__save__()
        return "<@{}> is removed from all queues!".format(ID)

# --------------------------------------------------------------------------------------------------
    def clearQueue(self, queueIdx):
        key = self.queuesName[queueIdx]
        self.queues[key] = []
        self.__save__()
        return "Queue of {} is cleared!".format(key)

# --------------------------------------------------------------------------------------------------
    def clearAll(self):
        self.queues = {i : [] for i in self.queuesName}
        self.__save__()
        return "ALL queues is cleared!"
                