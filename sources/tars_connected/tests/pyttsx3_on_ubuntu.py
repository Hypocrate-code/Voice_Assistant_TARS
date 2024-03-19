import pyttsx3 as tts
bot = tts.init()
bot.setProperty("rate", 180)
bot.say("Ceci est un test")
bot.runAndWait()