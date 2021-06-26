import sys
import json
try:
    from replit import db
    replit_db = True
except ImportError:
    replit_db = False


class WaitQueues:
    nameList = ['Boss 1', 'Boss 2', 'Boss 3', 'Boss 4', 'Boss 5', '持ち越し', '叫號未到']

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
                self.queues = {i : [] for i in self.nameList}
        else:
            try:
                with open(self.channelID + ".json", 'r', encoding='UTF-8') as file:
                    jsDict = json.load(file)
                self.queues = {i : jsDict[i] for i in self.nameList}
            except:
                self.queues = {i : [] for i in self.nameList}

# --------------------------------------------------------------------------------------------------
    def __save__(self):
        if (replit_db):
            db[self.channelID] = self.queues
        else:
            with open(self.channelID + ".json", "w", encoding='UTF-8') as file: 
                json.dump(self.queues, file, indent=4, ensure_ascii= False)


# --------------------------------------------------------------------------------------------------
    def __gettUsers__(self, queueIdx, number = sys.maxsize):
        key = self.nameList[queueIdx]
        users = []
        for [uID, uName] in self.queues[key]:
            users.append([uID, uName])
            number = number - 1
            if number == 0:
                break
        return users


# --------------------------------------------------------------------------------------------------
    def add(self, queueIdx, userID, userName):
        key = self.nameList[queueIdx]
        self.queues[key].append([userID, userName])
        self.__save__()

        if queueIdx == 6:
            return '<@{}> is add to **{}**'.format(userID, key)
        else:
            return '<@{}> is waiting for **{}**'.format(userID, key)

# --------------------------------------------------------------------------------------------------
    def delete(self, queueIdx, userID, userName):
        key = self.nameList[queueIdx]
        self.queues[key] = [i for i in self.queues[key] if i[0] != userID]
        self.__save__()
        return '<@{}> is removed from **{}**'.format(userID, key)

# --------------------------------------------------------------------------------------------------
    def show(self, queueIdx):
        key = self.nameList[queueIdx]
        users = self.__gettUsers__(queueIdx)

        userString = ''
        if len(users) > 0:
            for [uID, uName] in users:
                userString += uName + '🧍 '
        else:
            userString = 'Nobody '

        if queueIdx < len(self.nameList):
            return '**{}**: {}'.format(key, userString)

# --------------------------------------------------------------------------------------------------
    def showAll(self):
        message = ''
        for i in range(len(self.nameList)):
            message += self.show(i) + '\n'
        return message

# --------------------------------------------------------------------------------------------------
    def notifyNext(self, queueIdx):
        boss = self.nameList[queueIdx]
        nextBoss = (queueIdx + 1 ) % 5
        next2Boss = (queueIdx + 2 ) % 5
        message = '{} is dead.\n'.format(boss)

        # Notify next boss's queue
        users = self.__gettUsers__(nextBoss)
        if len(users) > 0:
            message += 'Ready to hit **{}** '.format(self.nameList[nextBoss])
            for [uID, uName] in users:
                message += '<@{}>'.format(uID)
            message += '\n'
            hightest = users[0]
        else:
            message += 'Nobody is waiting for **{}**\n'.format(self.nameList[nextBoss])
            hightest = None        

        # Notify next 2 boss's queue
        users = self.__gettUsers__(next2Boss, 1)
        if len(users) > 0:
            message += 'Prepare your party for **{}** '.format(self.nameList[next2Boss])
            for [uID, uName] in users:
                message += '<@{}>'.format(uID)
            message += '\n'

        return [message, hightest]

# --------------------------------------------------------------------------------------------------
    def carryOver(self, userID, userName):
        key = self.nameList[5]
        if [userID, userName] in self.queues[key]:
            self.queues[key] = [i for i in self.queues[key] if i[0] != userID]
            message = 'Your 持ち越し is removed'            
        else:
            self.queues[key].append([userID, userName])
            message = '{} is added to 持ち越し'.format(userName)
        return message

# --------------------------------------------------------------------------------------------------
    def needCarry(self):
        key = self.nameList[5]
        if len(self.queues[key]) > 0:
            message = 'Someone need 持ち越し '
            for [uID, uName] in self.queues[key]:
                message += '<@{}> '.format(uID)
        else:
            message = 'No one has 持ち越し'
        return message

# --------------------------------------------------------------------------------------------------
    def clearUser(self, userID):
        for key in self.nameList:
            self.queues[key] = [i for i in self.queues[key] if i[0] != userID]
        self.__save__()
        return '<@{}> is removed from all queues!'.format(userID)

# --------------------------------------------------------------------------------------------------
    def clearQueue(self, queueIdx):
        key = self.nameList[queueIdx]
        self.queues[key] = []
        self.__save__()
        return 'Queue of {} is cleared!'.format(key)

# --------------------------------------------------------------------------------------------------
    def clearAll(self):
        self.queues = {i : [] for i in self.nameList}
        self.__save__()
        return 'ALL queues is cleared!'
                