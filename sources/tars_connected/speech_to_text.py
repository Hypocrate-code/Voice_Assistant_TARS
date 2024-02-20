import sys


# from openai import OpenAI
import speech_recognition
# import pyttsx3 as tts

# from neuralintents.assistants import BasicAssistant

class Tars:
    def __init__(self):
        # pass
        # self.assistant = BasicAssistant("tars_connected/intents.json", method_mappings={ "print": self.print_un_truc})
        # self.assistant.fit_model(epochs=50)
        # self.assistant.save_model()

        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition

        while True:
            with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
                try:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=2)       # Se calibre pendant 2 sec pour en ignorer le son ambiant
                    print("Parlez...")
                    audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                    text = self.recognizer.recognize_google(audio, language="fr-FR")
                    text = text.lower()
                    print(f"J'ai entendu: \'\'\'\'{text}\'\'\'\'")
                
                    if text == "couper":
                        print("Au revoir !")
                        break

                    if "tarse" in text:
                        print("J'écoute ?...")
                        try:
                            self.recognizer.adjust_for_ambient_noise(mic, duration=2)       # Se calibre pendant 2 sec pour en ignorer le son ambiant
                            audio = self.recognizer.listen(mic)                 # Ecoute jusqu'à ce qu'il détecte un vide
                            text = self.recognizer.recognize_google(audio, language="fr-FR")
                            text = text.lower()

                            if text == "couper":
                                print("Au revoir !")
                                # self.assistant.stop()
                                # sys.exit()
                                break
                            # else:
                            #     if text is not None:
                                    # response = self.assistant.request(text)
                                    # if response is not None:
                                    #     print(response)

                        except speech_recognition.RequestError:
                            print("Error: API was unreachable or unresponsive")                      # API was unreachable or unresponsive

                        except speech_recognition.UnknownValueError:
                            print("Error: Unable to recognize speech, speech was unintelligible")              # speech was unintelligible

                except speech_recognition.RequestError:
                    print("Error: API was unreachable or unresponsive")                      # API was unreachable or unresponsive

                except speech_recognition.UnknownValueError:
                    print("Error: Unable to recognize speech, speech was unintelligible")              # speech was unintelligible
                
                text = None


Bot = Tars()



# client = OpenAI()
#
# audio_file = open("speech.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="text"
# )