import speech_recognition
import speech_synthesis
import os
import get_response
import luyin
import translation
import chat
import weather
import time
import DHT11
import fp_add
import fp_update
import detect_sleepy
import safebound

import pyautogui as pk
import pyperclip
from playsound import playsound
import RPi.GPIO as GPIO



light = 4
led = 23

def light_test():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,GPIO.LOW)
    if GPIO.input(light)==1:
        GPIO.output(led,GPIO.HIGH)
    else:
        GPIO.output(led,GPIO.LOW)

def say(content, isstr=True):
    if not content:
        print("内容为空")
        return
    path = speech_synthesis.tts(content, isstr)
    if path:
        os.system('mplayer ' + path)
    else:
        print('语音输出出现错误')

def trans(content):
    lansdict = {"中文":"zh", "英文":"en", "英语":"en"}
    '''pos = content.find("翻译")
    if pos==-1:
        pos = content.find("到")
        if pos==-1:
            return
        pos = content[pos:].find("翻译")
        if pos==-1:
            return'''
    source = None
    target = None
    sourcecode = None
    targetcode = None
    
    posdict = {}
    for lan in lansdict:
        posdict[lan] = content.find(lan)
    minp = len(content)
    minv = None
    for lan in posdict:
        if posdict[lan]!=-1 and posdict[lan]<minp:
            minp = posdict[lan]
            minv = lan
    if not minv:
        say("翻译的源语言或目标语言不明确")
        return
    source = minv
    sourcecode = lansdict[source]
    print("源语言是"+source)
    for lan in lansdict:
        if lan in content[minp+1:]:
            target = lan
            targetcode = lansdict[target]
            break

    if not target:
        say("翻译的源语言或目标语言不明确")
        return
    print("目标语言是"+target)
    if source==target:
        say("源语言和目标语言相同，不用翻译")
        return
    
    say(source+'翻译'+target+'的功能已开启，请输入要翻译的'+source+'对话')
    while True:
        luyin.recording('mysound.wav')
        trans_word = speech_recognition.stt('mysound.wav', lan=source)
        if trans_word:
            if '退出' in trans_word and "翻译" in trans_word:
                say("翻译功能已退出")
                return
            print('您要翻译的句子是'+trans_word)
            trans_res = translation.translation(trans_word, sourcecode, targetcode)
            return '这句话的'+target+'翻译是'+trans_res
        else:
            print('没有监听到正常的提问对话')
            say('没有监听到正常的提问对话。请输入要翻译的'+source+'对话')


def func_choose(old_sleepy_thread):
    light_test()
    say('您好，请问有什么可以帮到您？', True)
    luyin.recording('mysound.wav')
    stt_res = speech_recognition.stt('mysound.wav')
    
    sleepy_thread = None
    result = None
    if stt_res:
        print('您的提问是:', stt_res)
        if '天气' in stt_res:
            say("天气查询功能已经开启，请输入要查询的城市名")
            while True:
                luyin.recording('mysound.wav')
                city = speech_recognition.stt('mysound.wav')
                #city = '杭州'
                if city:
                    city = city.strip('。')
                    if '退出' in city and "查询" in city:
                        say("天气查询功能已退出")
                        return
                    print('您要查询的城市是'+city)
                    result = weather.get_weather(city)
                    if result:
                        break
                    say('没有监听到正确的城市。请重新输入要查询的城市名')
                else:
                    print('没有监听到正确的城市')
                    say('没有监听到正确的城市。请重新输入要查询的城市名')
            #result = weather.get_weather('杭州')
            # path = speech_synthesis.tts(wea, True)
        elif '几点' in stt_res or '时间' in stt_res:
            curtime = time.strftime("%Y年%m月%d日%H点%M分", time.localtime())
            result = '现在是' + curtime
            # path = speech_synthesis.tts('现在是' + curtime, True)
        elif '翻译' in stt_res:
            result = trans(stt_res)
            if not result:
                return
        elif "温度" in stt_res and "周围" in stt_res:
            print("正在检测中------")
            say("正在检测中")
            tem, humi = DHT11.get_tem(18)
            result = "当前周围的环境温度为" + str(tem) + "摄氏度。"
        elif "录入" in stt_res and "指纹" in stt_res:
            say("请按下指纹")
            result = fp_add.fp_add()
        elif "更新" in stt_res and "指纹" in stt_res:
            say("请按下指纹")
            result = fp_update.fp_update()
        elif "疲劳检测" in stt_res:
            if "打开" in stt_res or "开启" in stt_res:
                sleepy_thread = detect_sleepy.mythread_run()
                if not sleepy_thread:
                    result = "疲劳检测功能开启失败"
                else:
                    result = "成功开启疲劳检测功能"
            elif "关闭" in stt_res:
                if not old_sleepy_thread:
                    result = "当前未开启疲劳检测功能"
                else:
                    if detect_sleepy.mythread_stop(old_sleepy_thread):
                        result = "成功关闭疲劳检测功能"
                        sleepy_thread = 1
                    else:
                        result = "疲劳检测功能关闭失败"
        elif (("开启" in stt_res) or ("打开" in stt_res)) and "闲聊" in stt_res:
            say("闲聊功能已开启，你想聊点什么？")
            while True:
                luyin.recording('mysound.wav')
                myword = speech_recognition.stt('mysound.wav')
                print("myword:", myword)
                if not myword:
                    say("我没有听懂你说的话")
                    continue
                if (("退出" in myword) or ("关闭" in myword)) and \
                   "闲聊" in myword:
                    result = "闲聊功能已退出"
                    break
                say(get_response.get_response(myword))
        elif ("开始" in stt_res or "准备" in stt_res) and "开车" in stt_res:
            safebound.mythread_run()
            result = "end"
        elif "的女人" in stt_res:
            if "温柔" in stt_res:
                result = "雷艳静老师" + stt_res[1:len(stt_res)-1]
            elif "大方" in stt_res:
                result = "这还用说吗？当然还是雷艳静老师。"
            else:
                result = "你不用问了，只要是褒义词，都是形容雷艳静老师的"
        else:
            result = get_response.get_response(stt_res)
            # path = speech_synthesis.tts(response, True)
        if result != "end":
            if not result:
                say("未接收到合适指令")
            else:
                say(result)
    else:
        say('没有监听到正常的提问对话')
        return
    if sleepy_thread == 1:
        return None
    elif not sleepy_thread:
        return old_sleepy_thread
    else:
        return sleepy_thread

if __name__=='__main__':
    #GPIO_init()
    func_choose()

