import RPi.GPIO as GPIO
import time

import threading
import ctypes
import inspect

light = 4
led = 23

def mythread_run():
    global stop
    stop = False
    detect_thread = threading.Thread(target=led_test, args=())
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


def led_test():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,GPIO.LOW)
    while True:
        if GPIO.input(light)==1:
            GPIO.output(led,GPIO.HIGH)
        else:
            GPIO.output(led,GPIO.LOW)
 
        # print("--------light-----", GPIO.input(light))
        
