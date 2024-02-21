# import sys


import speech_recognition
# from openai import OpenAI
# import pyttsx3 as tts
# from neuralintents.assistants import BasicAssistant
from text_to_response import Tars_answering
# import text_to_response

def turn_in_red():
    print("> On a appelé turn_in_red")
    return
    # turn_in_red() est une foncion provisoire, qui devra être remplacée par un ACTIVATEUR de témoin d'écoute
def turn_in_black():
    print("> On a appelé turn_in_black")
    return
    # turn_in_black() est une foncion provisoire, qui devra être remplacée par un DESACTIVATEUR de témoin d'écoute
def say(text):
    print("> On a appelé say")
    return
    # say(text) est une fonction provisoire, qui devra être remplacée par un text to speech
def reponse_a_la_question(text):
    print("> On a appelé reponse_a_la_question")
    return
    # reponse_a_la_question(text) est une fonction provisoire, qui devra être remplacée par un text to response

class Tars:
    def __init__(self):
        # self.assistant = BasicAssistant("tars_connected/intents.json", method_mappings={ "print": self.print_un_truc})
        # self.assistant.fit_model(epochs=50)
        # self.assistant.save_model()

        self.tars = Tars_answering()
        self.mots_de_fin = ["couper", "arrêter", "stoppe", "stopper", "au revoir", "arrête"]
        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition

        with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
            while True:
                print("Parlez...")
                try:
                    audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    text = text.lower()
                    print(f"<{text}>")
                
                    if text in self.mots_de_fin:
                        print("Au revoir !")
                        return
                    
                    if "tarse " in text:
                        turn_in_red()
                        text = text.split("tarse ")[1]
                        print(f"\nVotre question: {text}\n")
                        self.tars.answer(text)
                        turn_in_black()
                    
                    elif "torse " in text:
                        turn_in_red()
                        text = text.split("torse ")[1]
                        print(f"\nVotre question: {text}\n")
                        say(reponse_a_la_question(text))
                        turn_in_black()

                    elif "tarse" in text or "torse" in text:
                        turn_in_red()
                        while True:
                            print("J'écoute ?...")
                            try:
                                audio = self.recognizer.listen(mic)           # Ecoute jusqu'à ce qu'il détecte un vide
                                text = self.recognizer.recognize_google(audio, language="fr-FR")
                                text = text.lower()

                                if text in self.mots_de_fin:
                                    print("Au revoir !")
                                    turn_in_black()
                                    return
                                else:
                                    print(f"\nVotre question: {text}\n")
                                    self.tars.answer(text)
                                    say(reponse_a_la_question(text))
                                    turn_in_black()
                                    break
                            except speech_recognition.RequestError:
                                print(">>>> Error: API was unreachable or unresponsive")          # API was unreachable or unresponsive
                                print(">>>> Problème de connexion avec l'API")

                            except speech_recognition.UnknownValueError:
                                print(">>>> Pardon, veuillez répéter")

                except speech_recognition.RequestError:
                    continue

                except speech_recognition.UnknownValueError:
                    continue





Bot = Tars()



# client = OpenAI()
#
# audio_file = open("speech.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="text"
# )