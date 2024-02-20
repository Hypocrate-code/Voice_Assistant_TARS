import sys


import speech_recognition
# from openai import OpenAI
# import pyttsx3 as tts
# from neuralintents.assistants import BasicAssistant

# import text_to_response

class Tars:
    def __init__(self):
        # pass
        # self.assistant = BasicAssistant("tars_connected/intents.json", method_mappings={ "print": self.print_un_truc})
        # self.assistant.fit_model(epochs=50)
        # self.assistant.save_model()

        self.mots_de_fin = ["couper", "arrêter", "stoppe", "stopper", "au revoir", "arrête"]
        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition

        with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
            print("Parlez...")
            while True:
                try:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=1)       # Se calibre pendant 2 sec pour en ignorer le son ambiant
                    audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    text = text.lower()
                    print(f"<{text}>")
                
                    if text in self.mots_de_fin:
                        print("Au revoir !")
                        break

                    if "tarse" in text:
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



# client = OpenAI()
#
# audio_file = open("speech.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="text"
# )