#coding: utf-8
import itchat

from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from base import robot
from base import common
from base import functions
#import getEmoj
#import os
from itchat.content import *
#from bs4 import BeautifulSoup
import configparser
from base import functions


# 加载配置文件
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

nameList = eval(config.get("object", 'TA'))                   # 对象们哦
morningFlag = eval(config.get("functions", "goodMorning"))    # 开启早晨问候，日期，天气情况，英文文摘，总开关
nightFlag = eval(config.get("functions", "goodNight"))        # 开启晚安模式开关
jokeFlag = eval(config.get("functions", "joke"))              # 午后小笑话开关
weatherFlag = eval(config.get("functions", "sendWeather"))    # 天气
DigestFlag = eval(config.get("functions", "sendDigest"))      # 文摘
heartFlag = eval(config.get("functions", "heartBeat"))        # 心跳机制
offworkFlag = eval(config.get("functions", "offWork"))
location = config.get("functions", "location")          # 城市名称

itchat.auto_login(hotReload=True)                       # 登入微信
whiteList = common.getWhiteList(itchat, nameList)       # 白名单列表名字的微信唯一标识
startRobot = False

@itchat.msg_register(itchat.content.TEXT)              # 智能闲聊
def rebot_relpy(msg):
    global startRobot
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"   "+msg["User"]["RemarkName"]+": "+msg["Text"])
    if msg["FromUserName"] in whiteList:
        if startRobot:
            if msg["Text"] == "再见":                            # 关闭聊天机器人
                startRobot = False
                return "主人再见"
            try:
                reply = robot.qqRobot(msg["Text"])
                if reply is None:
                    reply = robot.qingyunkeRobot(msg["Text"])
            except:
                reply = robot.qingyunkeRobot(msg["Text"])
            time.sleep(0.5)                                     # 延时，防止消息秒回，带点人性
            return reply

        else:
            if msg["Text"] == "宝贝精灵":                       # 唤醒聊天机器人
                startRobot = True
                return "在呢在呢~~"


def morningJob():
    functions.sendMorningMsg(itchat, nameList)

def noonJoke():
    functions.sendAjoke(itchat, nameList)

def eveningJob():
    functions.eveningGoodBye(itchat, nameList)

def offWork():
    functions.offwork(itchat,nameList)

def heartBeat():
    functions.heartbeat(itchat)


scheduler = BackgroundScheduler()
if morningFlag:
    scheduler.add_job(morningJob, 'cron', hour='7', minute='10' )   # 早上提醒
if jokeFlag:
    scheduler.add_job(noonJoke, 'cron',  hour='12', minute='30')     # 中午小笑话
if nightFlag:
    scheduler.add_job(eveningJob, 'cron', hour='22', minute='10')    # 晚上提醒
if offworkFlag:
    scheduler.add_job(offWork, 'cron', day_of_week="mon-fri", hour='10', minute='40') # 下班提醒
if heartFlag:
    scheduler.add_job(heartBeat, 'cron', minute='30, 00')      # 心跳提醒

scheduler.start()

while True:
    time.sleep(2)
    itchat.configured_reply()
