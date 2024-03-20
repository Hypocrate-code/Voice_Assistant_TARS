import threading

from local_web_server_for_config.app import app
from tars_connected.call_to_speech import TarsVocall
from tars_connected.utils import get_api_key, say_ip, set_audio_devices_on_launch

class Tars:
    def __init__(self):
        self.app = app
    def launch_tars(self):
        self.tars = TarsVocall()

if __name__ == '__main__':
    tars = Tars()
    set_audio_devices_on_launch()
    if get_api_key("openai"):
        tars_thread = threading.Thread(target=tars.launch_tars)
        tars_thread.start()
    else:
        tars_for_ip_thread = threading.Thread(target=say_ip)
        tars_for_ip_thread.start()
    tars.app.run(host="0.0.0.0", port=8000)

