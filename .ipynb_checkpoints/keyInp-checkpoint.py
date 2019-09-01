#just a file for keyboard module checking

from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def getSpace():
    global keyboard
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    return
    
