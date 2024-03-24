import subprocess
from tars_connected.utils import File, get_voice, get_api_key
from tars_connected.errors_response import api_key_invalid
from threading import Thread
from elevenlabs import generate, play, RateLimitError


class TarsSpeaker:
    def __init__(self):
        self.setup()
        self.are_generating = 0
        self.playing_queue = File()
        self.generating_queue = File()
        self.playing_queue_isworking = False
        self.generating_isworking = False

    def setup(self):
        self.voice = get_voice()

    def start_playing(self):
        self.playing_queue_isworking = True
        while not self.playing_queue.est_vide():
            to_say = self.playing_queue.defiler()
            if type(to_say) == type("exemple"):
                subprocess.call(["espeak", "-v", self.voice["spec"], '-s', '120', to_say])
            else:
                play(to_say)

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
                try:
                    audio = generate(
                        text=text,
                        model="eleven_multilingual_v1",
                        voice=self.voice["spec"],
                        api_key=get_api_key("elevenlabs")
                    )
                    self.are_generating -= 1
                    return audio
                except RateLimitError:
                    print("wtf")
                    while not self.generating_queue.est_vide():
                        print("défilement...")
                        self.generating_queue.defiler()
                    text = "Votre compte Elevenlabs n'a plus assez de caractères pour générer la phrase demandée, retour à la voix native. Rendez vous sur votre panneau de configuration pour plus d'infos."
                    api_key_invalid("elevenlabs", self, text=text)
                    break
                except Exception as e:
                    api_key_invalid("elevenlabs", self)
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
            if priority == 2:
                self.playing_queue.enfiler(text)
                if not self.playing_queue_isworking:
                    self.start_playing()

            elif priority == 1:
                self.playing_queue.mettre_premiere_place(text)
                if not self.playing_queue_isworking:
                    self.start_playing()
