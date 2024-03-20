# Useful functions across the project
import json
import os.path
import socket
import time


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def say_ip():
    from local_web_server_for_config.app import is_on_web_server
    from tars_connected.response_to_speech import TarsSpeaker
    speaker_for_ip = TarsSpeaker()
    while not (is_on_web_server):
        speaker_for_ip.say(f"Veuillez vous rendre via un navigateur connecté sur le même réseau à l'adresse web suivante : { get_ip_address().replace('.', ', point, ') }", 1)
        time.sleep(7)


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


def get_voice_spec():
    with open(os.path.dirname(__file__) + "/../user_config.json", encoding='utf-8') as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["tars voice spec"]


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
    prompt_system = f"Tu es Tars, un assistant vocal,à l'humour {humour_word} et au sarcasme {sarcasme_word}.N'utilise pas plus de {round(150 + 500 * (lenght / 100))} caractères,tu écris les nombres en lettre,pas en chiffre.Ne dis pas que tu es chat gpt."
    return prompt_system
