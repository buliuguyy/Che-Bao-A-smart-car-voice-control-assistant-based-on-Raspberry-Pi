#_*_ coding:UTF-8 _*_
# @author: zdl 
# 百度云语音合成Demo，实现对本地文本的语音合成。
# 需安装好python-SDK，待合成文本不超过1024个字节
# 合成成功返回audio.mp3 否则返回错误代码

# 导入AipSpeech  AipSpeech是语音识别的Python SDK客户端
from aip import AipSpeech
import os

''' 你的APPID AK SK  参数在申请的百度云语音服务的控制台查看'''
APP_ID = '23476319'
API_KEY = '6czQuWV4tavX9X0Gw2EHH4v5'
SECRET_KEY = 'LIpEcVha2ib082tlpoS0H9OjYZM3jGMp'

# 新建一个AipSpeech
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 将本地文件进行语音合成
def tts(filename, isstr=False):
    if isstr:
        word = filename
    else:
        f = open(filename,'r')
        command = f.read()
        if len(command) != 0:
            word = command
        f.close()
    if not word:
        return None
    result  = client.synthesis(word,'zh',1, {
        'vol': 5,'per':0,
    })
    print('语音内容: ', word)
# 合成正确返回audio.mp3，错误则返回dict
    if not isinstance(result, dict):
        with open('tts_result.mp3', 'wb') as f:
            f.write(result)
        f.close()
        return 'tts_result.mp3'
    return None

# main

if __name__ == '__main__':
    #tts('demo.txt', False)
    tts('您好，请问有什么可以帮到您？', True)
    os.system('mplayer audio.mp3')
