import sys
import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    return engine

def say(s):
    for i in range(3):
        engine.say(s)
        engine.runAndWait() # In here the program will wait as if is in main file

engine = init_engine()
say(str(sys.argv[1])) # Here it will get the text through sys from main file
