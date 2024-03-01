from flask import Flask, render_template, request, redirect, jsonify
from local_web_server_for_config.wifi_connexion import connect_to_wifi
from tars_connected.response_to_speech import Tars_vocal
import tars_connected.utils as utils
from elevenlabs import voices
import threading
import json

app = Flask(__name__)
app.tars_for_infos = Tars_vocal()
is_connected = None


# WEB PAGE OF THE SERVER

@app.route('/', methods=["POST", "GET"])
@app.route('/config', methods=["POST", "GET"])
def config():
    openai = utils.get_api_key("openai")
    if not (openai):
        return redirect("/openai")
    voice_spec = utils.get_voice_spec()
    voice = utils.get_voice()
    wifi_status = utils.get_wifi_status()
    print(voice)
    return render_template("config.html", humor=voice_spec['humor'], sarcasm=voice_spec["sarcasm"],
                           talkative=voice_spec["lenght of response"], wifi_status=wifi_status, voice=voice["origin"],
                           voice_type=voice["spec"], is_elevenlabs=not (utils.get_api_key("elevenlabs") == None),
                           list_of_elevenlabs_voices=voices(),
                           list_of_native_voices=["Voix masculine", "Voix féminine"])


@app.route('/wifi', methods=["POST", "GET"])
def wifi():
    if request.method == "POST":
        nom = request.form["ESSID"]
        code = request.form["password"]
        if nom == "" and code != "":
            return render_template("wifi.html", error_ssid="Veuillez compléter tous les champs.")
        elif nom != "" and code == "":
            return render_template("wifi.html", error_password="Veuillez compléter tous les champs.")
        if nom == "" and code == "":
            return render_template("wifi.html", error_password="Veuillez compléter tous les champs.",
                                   error_ssid="Veuillez compléter tous les champs.")
        elif len(code) < 8:
            return render_template("wifi.html", error_password="Le mot de passe est trop court.")
        else:
            test_connexion = threading.Thread(target=gate, args=(nom, code))
            test_connexion.start()
            while is_connected == None:
                pass
            if is_connected == 1:
                return render_template("wifi.html", error_password="Le mot de passe est incorrect.")
            elif is_connected == 10:
                return render_template("wifi.html", error_ssid="Le réseau n'est pas détecté.")
            elif is_connected == 0:
                return redirect("/config")
            else:
                print("WTFFF", is_connected)
                return redirect("/")
    else:
        return render_template('wifi.html')


# USEFUL FUNCTIONS AND API CALL

@app.route('/api/update_tars_spec', methods=["POST"])
def update_tars_spec():
    data = request.json
    print(data)
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        user_config["tars voice spec"] = data
        user_config["prompt_system"] = utils.update_prompt_system(data["humor"], data["sarcasm"],
                                                                  data["lenght of response"])
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()
    app.tars_for_infos.say("Personnalité de Tars mise à jour")
    return jsonify({'message': 'Personnalité de Tars mise à jour'}) \
 \
 \
@app.route('/api/update_tars_voice', methods=["POST"])
def update_tars_voice():
    data = request.json
    print(data)
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        user_config["voice"] = data
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()
    app.tars_for_infos.setup()
    if data["origin"] == "native":
        app.tars_for_infos.say("Ma voix est mise à jour")
    elif data["origin"] == "elevenlabs":
        app.tars_for_infos.say(f"Voix sélectionnée : {data['spec']}")
    return jsonify({'message': 'Voix de Tars mise à jour'})


def gate(nom, code):
    global is_connected
    is_connected = connect_to_wifi(nom, code)
