#coding: utf-8
import hashlib
from urllib import parse
import datetime
import requests
import json
import random
import string
import time
import marshal
import parser
import configparser

key1 = "e59454cf4e8e4bdb91eaa505083fd454"
key = "28fcc1e18e064e6d9aabac91ad57abc5"
key3 = "347b39ee228b4b109dae7270cc08d3c8"

config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")
app_id = config.get("robots", "app_id")       # 腾讯闲聊
app_key = config.get("robots","app_key")      # 腾讯闲聊
turingKey = config.get("robots","turingKey")

def turingRobot(msg):
    api = 'http://openapi.tuling123.com/openapi/api/v2'
    #为什么要以下格式，可以参看api文档
    dat = {
        "perception": {
            "inputText": {
                "text": msg
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": turingKey,
            "userId": "fool"
        }
    }
    try:
        dat = json.dumps(dat)
        r = requests.post(api, data=dat).json()
        #print(r)
        #print(r["results"][0]["values"]["text"])
        return r["results"][0]["values"]["text"]
    except:
        return "生病了，无法进行对话"





def qingyunkeRobot(mes):
    engine = "http://api.qingyunke.com/api.php?key=free&appid=0&msg="
    try:
        url = engine + mes
        r = requests.get(url).json()
        return (r["content"])
    except:
        return "出错了"





def qqRobot(text, userId=""):
    global app_id
    global  app_key
    URL = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

    """
    智能闲聊（腾讯）<https://ai.qq.com/product/nlpchat.shtml>
    接口文档：<https://ai.qq.com/doc/nlpchat.shtml>
    :param text: 请求的话
    :param userId: 用户标识
    :return: str
    """
    #try:

    # config.init()
    #info = config.get('auto_reply_info')['qqnlpchat_conf']

    app_id = app_id
    app_key = app_key
    if not app_id or not app_key:
        print('app_id 或 app_key 为空，请求失败, 正在启用备用机器人')
        return

    # 产生随机字符串
    nonce_str = ''.join(random.sample(
        string.ascii_letters + string.digits, random.randint(10, 16)))
    time_stamp = int(time.time())  # 时间戳
    params = {
        'app_id': app_id,  # 应用标识
        'time_stamp': time_stamp,  # 请求时间戳（秒级）
        'nonce_str': nonce_str,  # 随机字符串
        'session': "45678",  # 会话标识
        'question': text  # 用户输入的聊天内容
    }
    # 签名信息
    params['sign'] = getReqSign(params, app_key)
    try:
        resp = requests.post(URL, params=params)
       # print("resp"+resp)
        if resp.status_code == 200:
            #print(resp.text)
            content_dict = resp.json()
            if content_dict['ret'] == 0:
                data_dict = content_dict['data']
                return data_dict['answer']
            print('智能闲聊 获取数据失败:{}'.format(content_dict['msg']))
            return None
    except:
        # now = datetime.datetime.now()
        # errtime = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(
        #     now.minute) + "-" + str(now.second)
        # print("获取数据失败：key=%s"%text+"\t\t"+errtime)
        return None



def getReqSign(parser, app_key):
    '''
    获取请求签名，接口鉴权 https://ai.qq.com/doc/auth.shtml
    1.将 <key, value> 请求参数对按 key 进行字典升序排序，得到有序的参数对列表 N
    2.将列表 N 中的参数对按 URL 键值对的格式拼接成字符串，得到字符串 T（如：key1=value1&key2=value2），
        URL 键值拼接过程 value 部分需要 URL 编码，URL 编码算法用大写字母，例如 %E8，而不是小写 %e8
    3.将应用密钥以 app_key 为键名，组成 URL 键值拼接到字符串 T 末尾，得到字符串 S（如：key1=value1&key2=value2&app_key = 密钥)
    4.对字符串 S 进行 MD5 运算，将得到的 MD5 值所有字符转换成大写，得到接口请求签名
    :param parser: dect
    :param app_key: str
    :return: str,签名
    '''
    params = sorted(parser.items())
    uri_str = parse.urlencode(params, encoding="UTF-8")
    sign_str = '{}&app_key={}'.format(uri_str, app_key)
    # print('sign =', sign_str.strip())
    hash_md5 = hashlib.md5(sign_str.encode("UTF-8"))
    return hash_md5.hexdigest().upper()








#
# def run():
#     while True:
#
#         mes = input("me>")
#         if mes == "宝贝精灵":
#             print("在呢在呢~~")
#             while True:
#                 mes = input("me>")
#
#                 if mes != "再见":
#                     #anwser = turingRobot(mes)  # 图灵机器人
#                     #anwser = qingyunkeRobot(mes)  # 青园客机器人
#                     anwser = qqRobot(mes)
#                     print("robot>"+anwser)
#                 else:
#                     print("再见")
#                     break
#         else:
#             print("不做响应")
