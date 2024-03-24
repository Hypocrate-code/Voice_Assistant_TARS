# Useful functions across the project
import json
import socket
from urllib.request import urlopen
import time
import sounddevice as sd
import os
def make_sound(sound_file):
    os.system(f"aplay tars_connected/{sound_file}")
def get_ip_address():
    google = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((google, 0))
    addrIP = s.getsockname()[0]
    print(addrIP)
    return addrIP.replace('.',', point, ') + ", deux points 8000"


def say_ip(tars):
    from tars_connected.response_to_speech import TarsSpeaker
    speaker_for_ip = TarsSpeaker()
    while not (get_api_key("openai")):
        speaker_for_ip.say(
            f"Veuillez vous rendre via un navigateur connecté sur le même réseau à l'adresse web suivante : {get_ip_address().replace('.', ', point, ')}, deux points 8000",
            1)
        time.sleep(10)
    tars.launch_tars()


class File():
    def __init__(self):
        self.contenu = []

    def enfiler(self, objet):
        self.contenu.append(objet)

    def defiler(self):
        if len(self.contenu) > 0:
            objet = self.contenu[0]
            self.contenu = self.contenu[1:]
            return objet
        else:
            raise ("File déjà vide !")

    def est_vide(self):
        return len(self.contenu) == 0

    def taille(self):
        return len(self.contenu)

    def mettre_premiere_place(self, objet):
        self.contenu.insert(0, objet)


def get_audio_devices():
    mics = []
    speakers = []
    devices = sd.query_devices()
    with open("tars_connected/audio_devices_to_ignore.txt") as devices_to_ignore:
        list_of_devices_to_ignore = devices_to_ignore.read().split("\n")
        for device in devices:
            if device["max_input_channels"] > 0 and not (device["name"] in list_of_devices_to_ignore):
                mics.append(device["name"])
            if device["max_output_channels"] > 0 and (not (device["name"] in list_of_devices_to_ignore) or "default" in device["name"]):
                speakers.append(device["name"])
    return {"mics": mics, "speakers": speakers}


def get_saved_audio_devices():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["mic"], user_config_file["speaker"]


def set_audio_device(type_of_device, periph_name):
    index = sd.query_devices(periph_name)["index"]
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        if type_of_device == "input":
            sd.default.device = [index, sd.default.device[1]]
            user_config["mic"] = periph_name
        elif type_of_device == "output":
            sd.default.device = [sd.default.device[0], index]
            user_config["speaker"] = periph_name
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()

def set_audio_devices_on_launch():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        if user_config_file["mic"]:
            sd.default.device[0] = sd.query_devices(user_config_file["mic"])["index"]
        elif user_config_file["speaker"]:
            sd.default.device[1] = sd.query_devices(user_config_file["speaker"])["index"]

def get_api_key(origin):
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file[origin]


def get_voice():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["voice"]


def get_personality():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["tars personality"]


def get_wifi_status():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["wifi_configured"]


def get_prompt_system():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["prompt_system"]


def update_prompt_system(humour, sarcasme, lenght):
    level_words = {
        "0-4": "quasi inexistant",
        "5-9": "faible",
        "10-14": "léger",
        "15-19": "modéré",
        "20-24": "marginal",
        "25-29": "moyen",
        "30-34": "substantiel",
        "35-39": "assez présent",
        "40-44": "significatif",
        "45-49": "notable",
        "50-54": "important",
        "55-59": "élevé",
        "60-64": "conséquent",
        "65-69": "majeur",
        "70-74": "énorme",
        "75-79": "massif",
        "80-84": "critique",
        "85-89": "crucial",
        "90-94": "vital",
        "95-100": "extrême"
    }
    for numbers, word in level_words.items():
        liste_range = numbers.split("-")
        if int(liste_range[0]) <= humour <= int(liste_range[1]):
            humour_word = word
        if int(liste_range[0]) <= sarcasme <= int(liste_range[1]):
            sarcasme_word = word
    prompt_system = f"Tu es Tarsse, un assistant vocal,à l'humour {humour_word} et au sarcasme {sarcasme_word}.N'utilise pas plus de {round(150 + 500 * (lenght / 100))} caractères,tu écris les nombres en lettre,pas en chiffre.Ne dis pas que tu es chat gpt."
    return prompt_system
