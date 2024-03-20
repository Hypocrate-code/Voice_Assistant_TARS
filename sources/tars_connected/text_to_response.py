from tars_connected.response_to_speech import TarsSpeaker
from tars_connected.utils import get_api_key, get_prompt_system, get_voice
from tars_connected.errors_response import api_key_invalid

from threading import Thread
import winsound

from openai import OpenAI, AuthenticationError


class TarsAnswering:
    def __init__(self):
        self.api_key = get_api_key("openai")
        if not self.api_key:
            print("Vous n'avez pas de clé api openai")
        else:
            self.client = OpenAI(api_key=self.api_key)
            self.tars_vocal = TarsSpeaker()

    def answer(self, requete):
        try:

            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": get_prompt_system()},
                    {"role": "user", "content": requete}],
                stream=True,
            )

            response = ""

            for chunk in stream:
                if chunk.choices[0].delta.content != None and chunk.choices[0].delta.content != "":
                    response += chunk.choices[0].delta.content

                    for i, car in enumerate(response):

                        if car == " " and response[i - 1] == ".":
                            print(response[:(i + 1)])
                            if get_voice()["origin"] == "elevenlabs":
                                Thread(target=self.tars_vocal.say, args=(response[:(i + 1)], 2,)).start()
                            elif get_voice()["origin"] == "native":
                                self.tars_vocal.say(response[:(i + 1)], 2, )
                            response = response[(i + 1):]

            if response != "" and response != " ":
                print(response)

                if get_voice()["origin"] == "elevenlabs":
                    Thread(target=self.tars_vocal.say, args=(response[:(i + 1)], 2,)).start()

                elif get_voice()["origin"] == "native":
                    self.tars_vocal.say(response[:(i + 1)], 2, )


        except AuthenticationError:
            api_key_invalid("openai")
