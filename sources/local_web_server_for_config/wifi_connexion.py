import subprocess
def connect_to_wifi(ssid, password):
    connexion = subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password], capture_output=True)
    if connexion.returncode == 0:
        print("Connexion réussie")
    elif connexion.returncode == 10:
        print("Connexion échouée, le réseau n'est pas détécté.")
    elif connexion.returncode == 1:
        print("Connexion échouée, le mot de passe n'est pas bon.")
    else:
        print(connexion.returncode)