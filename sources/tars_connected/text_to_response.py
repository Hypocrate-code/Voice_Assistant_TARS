from tars_connected.utils import get_api_key

from openai import OpenAI, AuthenticationError
from tars_connected.errors_response import api_key_invalid

from tars_connected.response_to_speech import Tars_vocal



class Tars_answering:
    def __init__(self):
        self.client = OpenAI(api_key=get_api_key("openai"))
        self.tars_vocal = Tars_vocal()
    def answer(self, requete):
        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "Tu es Tars, un assistant vocal. N'utilise pas plus de 260 caractères, écris les chiffres en toute lettre."},
                    {"role": "user", "content": requete}
                ],
                stream=True
            )
            total = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    total+=chunk.choices[0].delta.content
            self.tars_vocal.say(total)
        except AuthenticationError:
            api_key_invalid("openai")



