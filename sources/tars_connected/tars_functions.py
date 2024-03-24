import json
from tars_connected.utils import get_ip_address, make_sound
def how_to_access(file):
    file.say("Vous pouvez me configurer en vous connectant à mon adresse IP, via une machine sur le même réseau que le mien.", 1)
def give_ip_address(file):
    file.say(f"Mon adresse IP est : {get_ip_address()}", 1)
def stop(file):
    make_sound('end_bip.wav')
# DO NOT TOUCH BELOW #
class FunctionRecognizer:
    def __init__(self, file):
        with open("tars_connected/functions_assignement.json") as functions_file:
            self.dict_of_functions = json.load(functions_file)
            self.file = file
    def recognize_functions(self, text):
        for tag, datas in self.dict_of_functions.items():
            for pattern in datas["patterns"]:
                if pattern in text:
                    globals()[datas["name of function"]](self.file)
                    return True
        return False
