import sounddevice as sd
import json
def set_audio_input(input=None, output=None):
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        if output:
            user_config["speaker"] = output
        if input:
            user_config["mic"] = input
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()
def get_audio_devices():
    devices = sd.query_devices()
    devices_to_return = {"Input": [], "Output": []}
    with open("default_sound_devices_to_ignore.txt") as defaults:
        default_devices_to_ignore = defaults.read().split("\n")
        for device in devices:
            if not(device["name"] in default_devices_to_ignore):
                devices_to_return["Input" if device["max_input_channels"] > 0 else "Output"].append(device["name"])
    return devices_to_return

def get_actual_devices():
    input_device = sd.default.device[0]
    output_device = sd.default.device[1]
    input_info = sd.query_devices(input_device)
    output_info = sd.query_devices(output_device)
    with open("default_sound_devices_to_ignore.txt") as defaults:
        devices_to_ignore = defaults.read().split("\n")
        if input_info["name"] in devices_to_ignore:
            input_device = None
        if output_info["name"] in devices_to_ignore:
            output_device = None
    return [input_device, output_device]

get_actual_devices()