from flask import Flask, render_template, request, redirect
from local_web_server_for_config.wifi_connexion import connect_to_wifi
import threading

app = Flask(__name__)
is_connected = None


@app.route('/', methods=["POST", "GET"])
@app.route('/config', methods=["POST", "GET"])
def config():
    if request.method == "POST":
        nom = request.form["ESSID"]
        code = request.form["password"]
        if nom == "" and code != "":
            return render_template("config.html", error_ssid="Veuillez compléter tous les champs.")
        elif nom != "" and code == "":
            return render_template("config.html", error_password="Veuillez compléter tous les champs.")
        if nom == "" and code == "":
            return render_template("config.html", error_password="Veuillez compléter tous les champs.", error_ssid="Veuillez compléter tous les champs.")
        elif len(code) < 8:
            return render_template("config.html", error_password="Le mot de passe est trop court.")
        else:
            test_connexion = threading.Thread(target=gate, args=(nom, code))
            test_connexion.start()
            while is_connected == None:
                pass
            if is_connected == 1:
                return render_template("config.html", error_password="Le mot de passe est incorrect.")
            elif is_connected == 10:
                return render_template("config.html", error_ssid="Le réseau n'est pas détecté.")
            elif is_connected == 0:
                return redirect("/good")
            else:
                print("WTFFF", is_connected)
                return redirect("/")
    else:
        return render_template('config.html')


@app.route('/good')
def good():
    return render_template("good.html")


def gate(nom, code):
    global is_connected
    is_connected = connect_to_wifi(nom, code)
