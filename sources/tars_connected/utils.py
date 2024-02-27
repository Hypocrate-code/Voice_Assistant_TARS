#Useful functions across the project
import json
def get_api_key(origin):
    with open("api_keys.json") as file:
        json_read = file.read()
        api_keys_file = json.loads(json_read)
        return api_keys_file[origin]

def get_voice_ai():
    with open("user_config.json") as file:
        json_read = file.read()
        user_config_file = json.loads(json_read)
        return user_config_file["voice"]