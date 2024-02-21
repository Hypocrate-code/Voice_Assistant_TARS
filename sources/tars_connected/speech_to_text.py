# import sys


import speech_recognition
# from openai import OpenAI
# import pyttsx3 as tts
# from neuralintents.assistants import BasicAssistant

# import text_to_response

# def turn_in_red():
#     print("> On a appelé turn_in_red")
#     return
#     turn_in_red() est une foncion provisoire, qui devra être remplacée par un ACTIVATEUR de témoin d'écoute
# def turn_in_black():
#     print("> On a appelé turn_in_black")
#     return
#     turn_in_black() est une foncion provisoire, qui devra être remplacée par un DESACTIVATEUR de témoin d'écoute
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

        self.mots_activation = ["tars", "tarse", "torse", "tarz"]
        self.mots_de_fin = ["couper", "arrêter", "stoppe", "stopper", "au revoir", "arrête"]
        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition

        with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
            self.recognizer.adjust_for_ambient_noise(mic, duration=4)
            while True:
                print("Parlez...")
                try:
                    audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    text = text.lower()
                    print(f"<{text}>")





                    for i in range(len(self.mots_activation)):
                        if self.mots_activation[i]+" " in text:
                            text = text.split(f"{self.mots_activation[i]} ")[1]
                            print(f"\nVotre question: {text}\n")
                            say(reponse_a_la_question(text))
                            break



                    if text in self.mots_de_fin or "fin de requête" in text:
                        print("Au revoir !")
                        return

                    elif self.mots_activation[0] in text or self.mots_activation[1] in text or self.mots_activation[2] in text or self.mots_activation[3] in text:
                        print("J'écoute ?...")
                        while True:
                            try:
                                audio = self.recognizer.listen(mic)           # Ecoute jusqu'à ce qu'il détecte un vide
                                text = self.recognizer.recognize_google(audio, language="fr-FR")
                                text = text.lower()

                                if text in self.mots_de_fin:
                                    print("Au revoir !")
                                    return
                                else:
                                    print(f"\nVotre question: {text}\n")
                                    say(reponse_a_la_question(text))
                                    break

                            except speech_recognition.RequestError:
                                print(">>>> Error: API was unreachable or unresponsive")          # API was unreachable or unresponsive
                                print(">>>> Problème de connexion avec l'API")

                            except speech_recognition.UnknownValueError:
                                print(">>>> Pardon, veuillez répéter")

                except speech_recognition.RequestError:
                    continue

                except speech_recognition.UnknownValueError:
                    print(">>>> Pardon, veuillez répéter")
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