import sys

import speech_recognition

from neuralintents.assistants import BasicAssistant

def turn_in_red():
    return
    # turn_in_red() est une foncion provisoire, qui devra être remplacée par un ACTIVATEUR de témoin d'écoute
def turn_in_black():
    return
    # turn_in_black() est une foncion provisoire, qui devra être remplacée par un DESACTIVATEUR de témoin d'écoute
def say():
    return
    # say(text) est une fonction provisoire, qui devra être remplacée par un text to speech
def reponse_a_la_question():
    return
    # reponse_a_la_question(text) est une fonction provisoire, qui devra être remplacée par un text to response

class Tars:
    def __init__(self):
        # pass
        # self.assistant = BasicAssistant("intents.json", method_mappings={ "print": self.print_un_truc})
        # self.assistant.fit_model(epochs=20)
        # self.assistant.save_model()

        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition

        while True:
            with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
                try:
                    audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    text = text.lower()
                    print(f"J'ai entendu: {text}")
                    if text == "couper":
                        print("Au revoir !")
                        return
                    
                    if "tarse " in text:
                        turn_in_red()
                        text = text.split("tarse ")[1]
                        say(reponse_a_la_question(text))
                        turn_in_black()
                    
                    elif "torse " in text:
                        turn_in_red()
                        text = text.split("torse ")[1]
                        say(reponse_a_la_question(text))
                        turn_in_black()

                    elif "tarse" in text or "torse" in text:
                        print("J'écoute ?...")
                        while True:
                            try:
                                self.recognizer.adjust_for_ambient_noise(mic, duration=1)       # Se calibre pendant 2 sec pour en ignorer le son ambiant
                                audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                                text = self.recognizer.recognize_google(audio, language="fr-FR")
                                text = text.lower()

                                if text in self.mots_de_fin:
                                    print("Au revoir !")
                                    # self.assistant.stop()
                                    # sys.exit()
                                    break
                                else:
                                    response = self.assistant.request(text)
                                    if response is not None:
                                        print(response)

                            except speech_recognition.RequestError:
                                print(">>>> Error: API was unreachable or unresponsive")                      # API was unreachable or unresponsive
                                print(">>>> Veuillez répéter")

                            except speech_recognition.UnknownValueError:
                                print(">>>> Error: Unable to recognize speech, speech was unintelligible")              # speech was unintelligible
                                print(">>>> Veuillez répéter")

                except speech_recognition.RequestError:
                    continue

                except speech_recognition.UnknownValueError:
                    continue





Bot = Tars()