#coding: utf-8
import json
import requests
import datetime
import os
import requests
import traceback
from bs4 import BeautifulSoup
import configparser
# 加载配置文件
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

weatherFlag = config.get("functions", "sendWeather")
digestFlag = config.get("functions", "sendDigest")
location = config.get("functions", "location")
year = eval(config.get("meet","year"))
month = eval(config.get("meet", "month"))
day = eval(config.get("meet", "day"))
tail = config.get("meet", "tail")
tailFlag = config.get("meet", "tailFlag")
'''
return a dict like: {'date': '28日星期四', 'high': '高温 12℃', 'fengli': '<![CDATA[3-4级]]>', 'low': '低温 9℃', 'fengxiang': '北风', 'type': '阴'}
'''
def getWeather(city):
    try:
        searchEngin = "http://wthrcdn.etouch.cn/weather_mini?city="
        r = requests.get(searchEngin+city).json()
        todayWeather = r['data']['forecast'][0]
        todayWeather.update({"ganmao":r["data"]["ganmao"]})
        #print("1"+str(todayWeather))
        return  todayWeather
    except:
        now = datetime.datetime.now()
        errtime = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(
            now.minute) + "-" + str(now.second)
        f = open("../log.file", "a+")
        f.write("获取天气失败\t\t" + errtime)
        f.close()
        return None


def getSentence():
    searchEngin = "http://open.iciba.com/dsapi"
    r = requests.get(searchEngin).json()
    return{"content":r["content"], "note":r["note"]}


def sendMessByNickname(itchat, nickName, msg):
    try:
        info = itchat.search_friends(nickName)[0]
        name = info["UserName"]
        itchat.send(msg, name)
        return 0
    except:
        return -1

def getWhiteList(itchat, nameList):
    whiteList = []
    for name in nameList:
        info = itchat.search_friends(name)
        if len(info) != 0:
            info=info[0]
            id = info["UserName"]
            whiteList.append(id)
    return whiteList


def getAll():
    global weatherFlag
    global digestFlag
    global location
    global  year
    global  month
    global day
    date = datetime.date.today()
    longtime = (datetime.date.today() - datetime.date(year, month, day)).days
    toSend = "早上好！\n\n今天是" + str(date.year) + "年" + str(date.month) + "月" + str(
        date.day) + "日" + " "
    if weatherFlag:
        weather = getWeather(location)                        # 获取天气情况
        if weather != None:
            week_day = weather['date'].split("日")[1]
            feng = weather["fengli"][9:-3] + "--" + weather["fengxiang"]
            toSend =toSend+week_day+"\n\n"
            toSend = toSend + "我们认识的第" + str(longtime) + "天" + "\n\n"
            toSend = toSend + "今日天气是" + weather['type'] + "\n" \
                     + "温度:" + weather['high'] + ", " + weather['low'] + "\n" \
                     + "风:" + feng + "\n\n"
            +weather["ganmao"] + "\n\n"
    if digestFlag:
        content = getSentence()                               # 获取文摘
        if content != None:
            toSend = toSend + content["content"] + "\n" + content["note"] + "\n\n"
        if tailFlag:
            toSend = toSend+"                   ---"+tail
        return toSend
    else:
        print("早晨推送失败")


#getAll()

def getUrlandText():
    site  = "http://wufazhuce.com/"
    try:
        r = requests.get(site)
        soup = BeautifulSoup(r.content, 'lxml')
        imgs = soup.find_all("img", class_="fp-one-imagen")
        # for img in imgs:          # the first one is update
        #     print(img.get("src"))
        url = imgs[0].get("src")
        sentence = soup.find("div", class_="fp-one-cita").find("a").string
        return url, sentence
    except:
        now = datetime.datetime.now()
        errtime = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(
            now.minute) + "-" + str(now.second)
        print("获取One数据失败\t\t" + errtime)
        return None, None


#print(getUrlandText())


def getImg(url, filename):

    global doneCount
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


def sendImgText(itchat, user):
    info = itchat.search_friends(user)[0]
    name = info["UserName"]
    imgName = "./img/"+str(datetime.date.today())+".jpg"
    url, text = getUrlandText()
    getImg(url, imgName)
  #  itchat.send_msg("(～﹃～)~zZ  夜话  (～﹃～)~zZ", name)
    itchat.send_image(imgName, name)
    itchat.send_msg(text, name)



'''
@itchat.msg_register(PICTURE)
def download_files(msg):
    tear = msg.fileName.split(".")[-1]
    msg.download("temp."+tear)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    cur_path = os.getcwd()
    img_path = os.path.join(cur_path, "temp."+tear)
    rt_img = "./emoji-mosaic.jpg"
    if os.path.exists(rt_img):
        os.remove(rt_img)
    getEmoj.getImage(img_path)
    return '@%s@%s' % (typeSymbol, rt_img)
'''



#getAll()


#getUrlandText()
