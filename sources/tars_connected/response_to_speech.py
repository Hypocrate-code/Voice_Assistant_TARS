import sys

import pyttsx3 as tts
from elevenlabs import generate, play, voices, stream
from elevenlabs.client import ElevenLabs
from utils import get_voice_ai, get_api_key

class Tars_vocal:
    def __init__(self):
        self.setup()
    def setup(self):
        self.voice = get_voice_ai()
        if self.voice == "native":
            self.speaker = tts.init()
            self.speaker.setProperty("rate", 150)
        elif self.voice == "elevenlabs":
            client = ElevenLabs(api_key=get_api_key("elevenlabs"))
    def say(self, something):
        if self.voice == "native":
            self.speaker.say(something)
            self.speaker.runAndWait()
        elif self.voice == "elevenlabs":
            audio = generate(
                text=something,
                model="eleven_multilingual_v1",
                voice="Rachel"
            )
            play(audio)
