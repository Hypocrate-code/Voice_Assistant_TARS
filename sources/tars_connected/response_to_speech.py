from utils import File_d_attente, get_voice, get_api_key

import pyttsx3 as tts
from elevenlabs import generate, play

class Tars_vocal:
    def __init__(self):
        self.setup()
        self.file = File_d_attente()
        self.is_waiting = 0
        self.are_generating = 0


    def setup(self):
        self.voice = get_voice()
        if self.voice['origin'] == "native":
            self.speaker = tts.init()
            self.speaker.setProperty("rate", 180)


    def say(self, text, numero):
        if self.voice['origin'] == "elevenlabs":
            self.file.enfiler(text)
            audio = generate(
                text=text,
                model="eleven_multilingual_v1",
                voice=self.voice["spec"],
                api_key=get_api_key("elevenlabs")
            )
            self.file.defiler()
            play(audio)

            while True:
                if self.is_waiting == numero:
                    play(audio)
                    self.is_waiting += 1
                    break




        elif self.voice['origin'] == "native":
            if self.speaker._inLoop:
                self.speaker.endLoop()
            self.speaker.say(text)
            self.speaker.runAndWait()