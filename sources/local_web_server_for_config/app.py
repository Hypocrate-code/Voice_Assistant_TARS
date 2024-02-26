from flask import Flask, render_template, request, redirect
from local_web_server_for_config.wifi_connexion import connect_to_wifi
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method =="POST":
        nom = request.form["name"]
        code = request.form["password"]
        if  nom == "" or code == "":
            print("veuillez complétez tous les champs")
        elif len(code) < 8:
            print("Le mot de passe n'est pas bon, il n'est pas assez long.")
        else:
            print(nom)
            print(code)
            connect_to_wifi(nom, code)
        return redirect("/")
    else:
        return render_template('config.html')
app.run(debug=True)