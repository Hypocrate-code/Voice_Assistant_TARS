import json
import threading
import time

from local_web_server_for_config.app import app
from tars_connected.response_to_speech import Tars_vocal
from tars_connected.call_to_speech import TarsVocall
from tars_connected.utils import get_api_key, get_ip_address

class Tars:
    def __init__(self):
        self.app = app
    def launch_tars_for_infos(self, message):
        self.tars_for_infos = Tars_vocal()
        self.tars_for_infos.say(message)
    def launch_tars(self):
        self.tars = TarsVocall()

if __name__ == '__main__':
    Tars = Tars()
    if get_api_key("openai"):
        thread_test = threading.Thread(target=Tars.launch_tars)
        thread_test.start()
    else:
        thread_test = threading.Thread(target=Tars.launch_tars_for_infos, args=(f"Veuillez vous connectez à : {get_ip_address()}",))
        thread_test.start()
    Tars.app.run(host="0.0.0.0", port=8000)

