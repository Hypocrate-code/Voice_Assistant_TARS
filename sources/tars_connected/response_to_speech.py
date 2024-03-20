import subprocess
from tars_connected.utils import FileDAattenteElevenlabs, get_voice, get_api_key
from elevenlabs import generate, play


class Tars_vocal:
    def __init__(self):
        self.setup()
        self.file = FileDAattenteElevenlabs()
        self.is_waiting = 0
        self.are_generating = 0

    def setup(self):
        self.voice = get_voice()

    def say(self, text):
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



        elif self.voice['origin'] == "native":
            subprocess.call(["espeak", "-v", self.voice["spec"], '-s', '160', text])
