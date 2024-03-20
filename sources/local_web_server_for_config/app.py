from flask import Flask, render_template, request, redirect, jsonify
from local_web_server_for_config.wifi_connexion import connect_to_wifi
from tars_connected.response_to_speech import TarsSpeaker
import tars_connected.utils as utils
from elevenlabs import voices
import threading
import json
import copy
from openai import OpenAI, AuthenticationError
import sounddevice as sd

app = Flask(__name__)
app.tars_for_infos = TarsSpeaker()
is_connected = None


# WEB PAGE OF THE SERVER

@app.route('/', methods=["POST", "GET"])
@app.route('/config', methods=["POST", "GET"])
def config():
    openai = utils.get_api_key("openai")
    if not openai:
        return redirect("/openai")
    personality = utils.get_personality()
    voice = utils.get_voice()
    wifi_status = utils.get_wifi_status()
    if voice["origin"] == "native":
        label = "Voix masculine" if voice["spec"] == "mb-fr1" else "Voix féminine"
    else:
        label = voice["spec"]
    return render_template("config.html", humor=personality['humor'], sarcasm=personality["sarcasm"],
                           talkative=personality["lenght of response"], wifi_status=wifi_status, audio_devices=utils.get_audio_devices(),
                           saved_audio_devices = utils.get_saved_audio_devices(), voice=voice["origin"],
                           voice_name=label, is_elevenlabs=not (utils.get_api_key("elevenlabs") is None),
                           list_of_elevenlabs_voices=voices(),
                           list_of_native_voices=["Voix masculine", "Voix féminine"])


@app.route('/openai', methods=["POST", "GET"])
def openai_page():
    if request.method == "POST":
        try:
            client = OpenAI(api_key=request.form["api-key"])
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "user", "content": "Say test"}
                ]
            )
            if response:
                with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
                    user_config = json.load(user_config_file)
                    user_config["openai"] = request.form["api-key"]
                    user_config_file.seek(0)
                    json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
                    user_config_file.truncate()
                return redirect("/")
        except:
            return render_template('openai.html', error_key="La clé rentrée n'est pas valide.")
    else:
        return render_template('openai.html')


@app.route('/elevenlabs', methods=["POST", "GET"])
def elevenlabs_page():
    openai = utils.get_api_key("openai")
    if not (openai):
        return redirect("/openai")
    if request.method == "POST":
        with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
            user_config = json.load(user_config_file)
            original_voice = copy.deepcopy(user_config["voice"])
            user_config["elevenlabs"] = request.form["api-key"]
            user_config["voice"]["origin"] = "elevenlabs"
            user_config["voice"]["spec"] = "Nicole"

            print("fdsufds2", original_voice)
            user_config_file.seek(0)
            json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
            user_config_file.truncate()
        try:
            app.tars_for_infos.setup()
            app.tars_for_infos.say("Configuration réussie.")
            with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
                user_config = json.load(user_config_file)
                user_config["voice"] = original_voice
                user_config_file.seek(0)
                json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
                user_config_file.truncate()
            return redirect("/")
        except Exception as e:
            print(e)
            with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
                user_config = json.load(user_config_file)
                user_config["elevenlabs"] = None
                print(original_voice)
                user_config["voice"] = original_voice
                user_config_file.seek(0)
                json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
                user_config_file.truncate()
            return render_template('elevenlabs.html', error_key="Votre clé API est invalide.")
    else:
        return render_template('elevenlabs.html')


@app.route('/wifi', methods=["POST", "GET"])
def wifi():
    openai = utils.get_api_key("openai")
    if not (openai):
        return redirect("/openai")
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


@app.route("/comment_créer_une_clé_api_elevenlabs")
def create_api_key_elevenlabs_page():
    return render_template("create-elevenlabs-api-key.html")\

@app.route("/comment_créer_une_clé_api_openai")
def create_api_key_openai_page():
    return render_template("create-openai-api-key.html")

# USEFUL FUNCTIONS AND API CALL

@app.route('/api/update_tars_personality', methods=["POST"])
def update_tars_spec():
    data = request.json
    print(data)
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        user_config["tars personality"] = data
        user_config["prompt_system"] = utils.update_prompt_system(data["humor"], data["sarcasm"],
                                                                  data["lenght of response"])
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()
    app.tars_for_infos.say("Personnalité de Tarsse mise à jour", 1)
    return jsonify({'message': 'Personnalité de Tars mise à jour'})


@app.route('/api/update_tars_voice', methods=["POST"])
def update_tars_voice():
    data = request.json
    with open('user_config.json', 'r+', encoding='utf-8') as user_config_file:
        user_config = json.load(user_config_file)
        user_config["voice"] = data
        user_config_file.seek(0)
        json.dump(user_config, user_config_file, indent=2, ensure_ascii=False)
        user_config_file.truncate()
    app.tars_for_infos.setup()
    if data["origin"] == "native":
        app.tars_for_infos.say("Ma voix est mise à jour", 1)
    elif data["origin"] == "elevenlabs":
        app.tars_for_infos.say(f"Voix sélectionnée : {data['spec']}", 1)
    return jsonify({'message': 'Voix de Tars mise à jour'})


@app.route('/api/update_tars_periph', methods=["POST"])
def update_audio_devices():
    periph = request.json
    type_of_device = "input" if sd.query_devices(periph)["max_input_channels"] > 0 else "output"
    utils.set_audio_device(type_of_device, periph)
    print(periph)
    return "Periphérique mis à jour."


def gate(nom, code):
    global is_connected
    is_connected = connect_to_wifi(nom, code)
