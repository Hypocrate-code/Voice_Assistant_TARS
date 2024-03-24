import json
from tars_connected.utils import get_ip_address, make_sound
import datetime
from num2words import num2words

# YOUR FUNCTIONS
def how_to_access(file, text):
    file.say("Vous pouvez me configurer en vous connectant à mon adresse IP, via une machine sur le même réseau que le mien.", 1)
def give_ip_address(file, text):
    file.say(f"Mon adresse IP est : {get_ip_address()}", 1)
def stop(file, text):
    while not file.playing_queue.est_vide():
        file.playing_queue.defiler()
    while not file.generating_queue.est_vide():
        file.generating_queue.defiler()
    make_sound('end_bip.wav')
def what_time(file, text):
    instant_actuel = datetime.datetime.now()
    heure = num2words(instant_actuel.hour, lang='fr')
    minute = num2words(instant_actuel.minute, lang='fr')
    jour = num2words(instant_actuel.day, lang='fr')
    liste_des_mois = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
    mois = liste_des_mois[instant_actuel.month - 1]
    annee = num2words(instant_actuel.year, lang='fr')
    file.say(f"Nous sommes le {jour} {mois} {annee}, il est {heure} heures {minute}.", 1)

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
                    globals()[datas["name of function"]](self.file, text)
                    return True
        return False
