import subprocess
import time
def connect_to_wifi(ssid, password):
    connexion = subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password], capture_output=True)
    return connexion.returncode
