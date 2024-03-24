import json
from tars_connected.utils import say_ip
def api_key_invalid(origin, TarsSpeaker, text = None):
    print(f"Your {origin} key is invalid")
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        user_config[origin] = None
        if origin == "elevenlabs":
            user_config["voice"] = {
                "origin": "native",
                "spec": "mb-fr1"
            }
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()

    TarsSpeaker.setup()
    TarsSpeaker.say(f"Votre clé API {origin} est invalide.", 1)
    if origin == "elevenlabs":
        TarsSpeaker.say(text, 2)
    else:
        from start_tars import Tars
        say_ip(Tars)

