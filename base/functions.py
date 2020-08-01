from base import common
from base import robot
import datetime

def sendMorningMsg(itchat, nameList):
    itchat.send(common.getAll(), 'filehelper')
    for name in nameList:
        common.sendMessByNickname(itchat, name, common.getAll())

def  offwork(itchat, nameList):
    for name in nameList:
        common.sendMessByNickname(itchat, name, "下班了，啦啦啦")


def heartbeat(itchat):
    if itchat.check_login() != "200":
        print("error: not login")
        try:
            itchat.auto_login(hotReload=True)
        except:
            exit(1)
    itchat.send(" I am alive", 'filehelper')

def writeLog():
    now = datetime.datetime.now()
    errtime = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
    f = open("../log.file", "a+")
    f.write(" robot is working fine\t\t"+errtime+"\n")
    f.close()

def eveningGoodBye(itchat, nameList):
    try:
        for name in nameList:
            common.sendImgText(itchat,name)
    except:
        pass

def sendAjoke(itchat, nameList):
    try:
        joke = robot.qqRobot("讲个笑话吧")
        for name in nameList:
            common.sendMessByNickname(itchat, name, joke)
    except:
        pass