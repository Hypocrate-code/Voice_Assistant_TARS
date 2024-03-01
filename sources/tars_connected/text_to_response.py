from tars_connected.utils import get_api_key

from openai import OpenAI, AuthenticationError
from tars_connected.utils import get_prompt_system
from tars_connected.errors_response import api_key_invalid
from tars_connected.response_to_speech import Tars_vocal


class Tars_answering:
    def __init__(self):
        self.api_key = get_api_key("openai")
        if not self.api_key:
            print("Vous n'avez pas de clé api openai")
        else:
            self.client = OpenAI(api_key=self.api_key)
            self.tars_vocal = Tars_vocal()

    def answer(self, requete):
        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system",
                     "content": get_prompt_system()},
                    {"role": "user", "content": requete}
                ],
                stream=True
            )
            total = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    total += chunk.choices[0].delta.content
            self.tars_vocal.say(total)
        except AuthenticationError:
            api_key_invalid("openai")
bot = Tars_answering()
bot.answer("Qui es tu ?")
