import sys
import pyttsx3 as tts
from elevenlabs import generate, play, stream
from tars_connected.utils import get_voice, get_api_key
class Tars_vocal:
    def __init__(self):
        self.setup()
    def setup(self):
        self.voice = get_voice()
        if self.voice['origin'] == "native":
            self.speaker = tts.init()
            self.speaker.setProperty("rate", 200)
    def say(self, something, test):
        if self.voice['origin'] == "native":
            if self.speaker._inLoop:
                self.speaker.endLoop()
            self.speaker.say(something)
            self.speaker.runAndWait()
        elif self.voice['origin'] == "elevenlabs":
            audio = generate (
                text=something,
                model="eleven_multilingual_v1",
                voice=self.voice["spec"]
            )
            play(audio)

