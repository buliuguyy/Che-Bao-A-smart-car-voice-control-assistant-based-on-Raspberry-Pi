import speech_recognition
import speech_synthesis
import os
import get_response
import luyin
import Main
import LED
import RPi.GPIO as GPIO

import snowboydecoder
import sys
import signal

interrupted = False
detect_sleepy_thread = None

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def detected():
    global detect_sleepy_thread
    print("--------------------------------")
    detect_sleepy_thread = Main.func_choose(detect_sleepy_thread)


def safebound_init(sender, receiver):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sender,GPIO.OUT)
    GPIO.setup(receiver, GPIO.OUT)
    GPIO.output(receiver,GPIO.LOW)
    GPIO.output(sender,GPIO.HIGH)

LED.mythread_run()
# safebound_init(20, 21)

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detected,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()