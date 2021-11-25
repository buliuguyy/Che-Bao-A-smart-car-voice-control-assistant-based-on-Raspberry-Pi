import requests

def get_weather(city):
    try:
        url = 'http://wthrcdn.etouch.cn/weather_mini?city='+city
        respj = requests.get(url).json()
        data = respj.get('data').get('forecast')
        content = '今天' + city + '的天气。' + data[0].get('type') + '。' + \
            '最低温度' + data[0].get('low').split()[1] + '。' + \
            '最高温度' +  data[0].get('high').split()[1] + '。' + \
            data[0].get('fengxiang') + str(data[0].get('fengli'))[9:11]
        content2 =  '明天' + city + '的天气。' + data[1].get('type') + '。' + \
            '最低温度' + data[1].get('low').split()[1] + '。' + \
            '最高温度' +  data[1].get('high').split()[1] + '。' + \
            data[1].get('fengxiang') + str(data[1].get('fengli'))[9:11]
        return content + '。' + content2
    except:
        return None

if __name__=='__main__':
    print(get_weather('杭州'))