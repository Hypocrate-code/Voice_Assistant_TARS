import json
from utils import get_ip_address
def how_to_access(file):
    file.say("Vous pouvez me configurer en vous connectant à mon adresse IP, via une machine sur le même réseau que le mien.")
def give_ip_address(file):
    file.say("Mon adresse est :", get_ip_address())

# DO NOT TOUCH BELOW #
class FunctionRecognizer:
    def __init__(self, file):
        with open("tars_connected/functions_assignement.json") as functions_file:
            self.dict_of_functions = json.load(functions_file)
            self.file = file
            print(self.dict_of_functions)
    def recognize_functions(self, text):
        for tag, datas in self.dict_of_functions.items():
            for pattern in datas["patterns"]:
                if pattern in text:
                    globals()[datas["name of function"]](self.file)
                    return True
        return False
