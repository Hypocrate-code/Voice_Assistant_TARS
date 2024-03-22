from tars_connected.utils import get_api_key, get_prompt_system, get_voice
from tars_connected.errors_response import api_key_invalid
from local_web_server_for_config.app import app

from threading import Thread


from openai import OpenAI, AuthenticationError


class TarsAnswering:
    def __init__(self):
        self.api_key = get_api_key("openai")
        if not self.api_key:
            print("Vous n'avez pas de clé api openai")
        else:
            self.client = OpenAI(api_key=self.api_key)
            self.tars_vocal = app.tars_for_infos

    def answer(self, requete):
        try:

            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": get_prompt_system()},
                    {"role": "user", "content": requete}],
                stream=True,
            )

            total = ""

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    if '.' in chunk.choices[0].delta.content:
                        total = total + chunk.choices[0].delta.content.split(".")[0] + "."
                        print(total)
                        actual = Thread(target=self.tars_vocal.say, args=(total,2,))
                        actual.start()
                        total = chunk.choices[0].delta.content.split(".")[1]
                    else:
                        total += chunk.choices[0].delta.content
            if not(total == "" or total == " "):
                actual = Thread(target=self.tars_vocal.say, args=(total,2,))
                actual.start()
            Thread(target=self.tars_vocal.say, args=(total,2,))

        except AuthenticationError:
            api_key_invalid("openai")
