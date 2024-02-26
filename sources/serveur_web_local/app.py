from flask import Flask, render_template, request, redirect
from serveur_web_local.wifi_connexion import connect_to_wifi
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method =="POST":
        nom = request.form["name"]
        code = request.form["password"]
        if  nom == "" or code == "":
            print("veuillez complétez tous les champs")
        else:
            print(nom)
            print(code)
            connect_to_wifi(nom, code)
        return redirect("/")
    else:
        return render_template('base.html')

