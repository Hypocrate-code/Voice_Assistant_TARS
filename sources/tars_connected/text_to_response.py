from response_to_speech import Tars_vocal
from utils import get_api_key, get_prompt_system, get_voice
from errors_response import api_key_invalid

from threading import Thread

from openai import OpenAI, AuthenticationError, ChatCompletion
from elevenlabs import generate, stream



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
                    {"role": "system", "content": get_prompt_system()},
                    {"role": "user", "content": requete}],
                stream=True,
            )


            

            nombre_de_mots_voulus = 0                   # 0 --> Phrase par phrase       # x --> x mots par x mots




            if nombre_de_mots_voulus > 0:
                response = ""

                for chunk in stream:
                    if chunk.choices[0].delta.content != None and chunk.choices[0].delta.content != "":
                        response += chunk.choices[0].delta.content

                        nb_spaces = 0
                        for i, car in enumerate(response):

                            if car == " ":
                                nb_spaces += 1

                                if nb_spaces >= 9:
                                    thread = Thread(target=self.tars_vocal.say, args=(response[:(i+1)], 2,))
                                    thread.start()
                                    print(response[:(i+1)])
                                    response = response[(i+1):]
                                    break


                if response != "" and response != " ":
                    thread = Thread(target=self.tars_vocal.say, args=(response[:(i+1)], 2,))
                    thread.start()
                    print(response)





            else:
                response = ""

                for chunk in stream:
                    if chunk.choices[0].delta.content != None and chunk.choices[0].delta.content != "":
                        response += chunk.choices[0].delta.content

                        for i, car in enumerate(response):
                            if car == " " and response[i-1] == ".":
                                thread = Thread(target=self.tars_vocal.say, args=(response[:(i+1)], 2,))
                                thread.start()
                                print(response[:(i+1)])
                                response = response[(i+1):]

                if response != "" and response != " ":
                    thread = Thread(target=self.tars_vocal.say, args=(response[:(i+1)], 2,))
                    thread.start()
                    print(response)






        except AuthenticationError:
            api_key_invalid("openai")
        
        # Test pour l'interruption
        from time import sleep
        sleep(15)
        Thread(target=self.tars_vocal.say, args=("La voix de TARS a été changée", 1,)).start()

Bot = Tars_answering()
Bot.answer("En 6 phrases, peux tu me donner ton pronostique pour ma note de philosophie par rapport à l'examen de ce matin, et pourquoi ?")