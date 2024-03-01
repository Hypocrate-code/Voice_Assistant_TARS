import json
import threading
from local_web_server_for_config.app import app
from tars_connected.response_to_speech import Tars_vocal
from tars_connected.speech_to_text import Tars_recognizer

class Tars:
    def __init__(self):
        self.app = app
    def launch_tars_for_infos(self):
        self.tars_for_infos = Tars_vocal()
    def launch_tars(self):
        self.tars = Tars_recognizer()


if __name__ == '__main__':
    Tars = Tars()
    thread_for_tars_infos = threading.Thread(target=Tars.launch_tars_for_infos)
    Tars.app.run(host="0.0.0.0", debug=True, port=8000)


