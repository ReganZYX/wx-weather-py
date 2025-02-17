import os
import random
from datetime import date, datetime

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# 当前日期
today = datetime.now()

# 微信公众号 app_id
app_id = os.environ["APP_ID"]

# 微信公众号 app_secret
app_secret = os.environ["APP_SECRET"]

# 彩虹屁接口密钥 key
key = os.environ["KEY"]

# 微信公众号 模板id
template_id = os.environ["TEMPLATE_ID"]

# 用户列表 也可通过接口获取，但是接口获取的只有用户id没有用户昵称，不方便部分数据展示，如果有新增人员，对应添加一个user对象即可
'''
    user_id: 微信公众号的 openid
       name: 昵称
       date: 相识日期
   birthday: 生日
       city: 城市编码，api接口文档处查询
'''
user_id_list = [
    {'user_id': 'osF4X6BWStR__0yh91O_pLH2TJl4',
     'city': '130600'}
]


# 彩虹屁
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    result = words.json()['data']['text']
    print(result)
    return result


# 文字颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 天气信息
def get_weather(city):
    url = "https://restapi.amap.com/v3/weather/weatherInfo?output=JSON&key=" + key + "&city=" + city
    res = requests.get(url).json()
    print(res)
    weather = res["lives"][0]
    return weather['weather'], weather['temperature'], weather['winddirection'], weather['province'] + weather[
        'city']


# 发送消息 支持批量用户
def send_message():
    for user in user_id_list:
        user_id = user.get('user_id')
        city = user.get('city')
        print(user_id)

        wea, temperature, winddirection, cityName = get_weather(city)

        client = WeChatClient(app_id, app_secret)

        wm = WeChatMessage(client)

        data = {
            "weather": {"value": wea, "color": get_random_color()},
            "temperature": {"value": temperature + "℃", "color": get_random_color()},
            "cityname": {"value": cityName, "color": get_random_color()},
            "winddirection": {"value": winddirection, "color": get_random_color()},
            "words": {"value": get_words(), "color": get_random_color()}
        }
        res = wm.send_template(user_id, template_id, data)
        print(res)


send_message()
