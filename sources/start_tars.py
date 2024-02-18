import json

from local_web_server_for_config.app import app
from tars_connected.speech_to_text import Tars

if __name__ == '__main__':
    with open("user_config.json") as user_config_file:
        user_config_read = user_config_file.read()
        user_config = json.loads(user_config_read)
    if user_config["problem_or_start_up"]:
        app.run(debug=True, port="5000")
    else:
        Tars()