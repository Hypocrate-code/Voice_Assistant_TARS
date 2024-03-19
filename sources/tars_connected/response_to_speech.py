from utils import File, get_voice, get_api_key

from threading import Thread

import pyttsx3 as tts
from elevenlabs import generate, play

class Tars_vocal:
    def __init__(self):
        self.setup()
        self.is_waited = 0
        self.are_generating = 0
        self.playing_queue = File()
        self.generating_queue = File()
        self.playing_queue_isworking = False
        self.generating_isworking = False


    def setup(self):
        self.voice = get_voice()
        if self.voice['origin'] == "native":
            self.speaker = tts.init()
            self.speaker.setProperty("rate", 200)

    def start_playing(self):
        self.playing_queue_isworking = True

        while not self.playing_queue.est_vide():
            play(self.playing_queue.defiler())

        self.playing_queue_isworking = False
    
    def start_generating(self):
        self.generating_isworking = True

        while not self.generating_queue.est_vide():
            audio = self.generate_audio((self.generating_queue.defiler()))
            self.playing_queue.enfiler(audio)

            if not self.playing_queue_isworking:
                Thread(target=self.start_playing).start()

        self.generating_isworking = False
    
    def generate_audio(self, text):
        while True:

            if self.are_generating < 2:
                self.are_generating += 1

                audio = generate(
                    text=text,
                    model="eleven_multilingual_v1",
                    voice=self.voice["spec"],
                    api_key=get_api_key("elevenlabs")
                )

                self.are_generating -= 1

                return audio

    def say(self, text, priority):
        if self.voice['origin'] == "elevenlabs":

            if priority == 2:
                self.generating_queue.enfiler(text)
                if not self.generating_isworking:
                    self.start_generating()

            elif priority == 1:
                audio = self.generate_audio(text)
                self.playing_queue.mettre_premiere_place(audio)
                if not self.playing_queue_isworking:
                    self.start_playing()
                





        elif self.voice['origin'] == "native":
            if self.speaker._inLoop:
                self.speaker.endLoop()
            self.speaker.say(text)
            self.speaker.runAndWait()