import threading
import ctypes
import inspect

import RPi.GPIO as GPIO
import time

import speech_synthesis
import os

sender = 20
receiver = 21

def say(content, isstr=True):
    if not content:
        print("内容为空")
        return
    path = speech_synthesis.tts(content, isstr)
    if path:
        os.system('mplayer ' + path)
    else:
        print('语音输出出现错误')

def mythread_run():
    global stop
    stop = False
    detect_thread = threading.Thread(target=safebound_test, args=())
    detect_thread.start()
    return detect_thread.ident

def mythread_stop(thread_ident):
    global stop
    stop = True
    time.sleep(10)
    stop_thread(thread_ident)
    return True


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)


def stop_thread(thread_ident):
    """终止线程"""
    _async_raise(thread_ident, SystemExit)
    # print("stop successful!")



def safebound_test():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(receiver,GPIO.IN)
    #GPIO.setup(sender, GPIO.IN)
    while True:
        #print(receiver, "端口电平为：", GPIO.input(receiver),)#'     ', sender, "端口电平为：", GPIO.input(sender))
        
        for i in range(100):
            if GPIO.input(receiver)==0:
                # print("安全带已系好")
                break
        else:
            print("安全带未系好")
            say("安全带未系好,禁止开车！")

        

