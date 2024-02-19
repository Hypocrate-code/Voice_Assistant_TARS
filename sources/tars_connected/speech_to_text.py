import sys


# from openai import OpenAI
import speech_recognition
import pyttsx3 as tts

from neuralintents.assistants import BasicAssistant

class Tars:
    def print_un_truc():
        print("salut gros")
    def __init__(self):
        pass
        self.recognizer = speech_recognition.Recognizer()           # Initialiser Speech Recognition
        self.assistant = BasicAssistant("tars_connected/intents.json", method_mappings={ "print": self.print_un_truc})
        self.assistant.fit_model(epochs=50)
        self.assistant.save_model()
        while True:
        
            with speech_recognition.Microphone() as mic:            # Avec le microphone par défaut
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                text = text.lower()
                if text != "":
                    print("Heard something !")
                if "hey tars" in text:
                    print("heyyyy tars")
                    audio = self.recognizer.listen(mic)
                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()
                    if text == "stop":
                        print("c'est ciao")
                        self.assistant.stop()
                        sys.exit()
                    else:
                        if text is not None:
                            response = self.assistant.request(text)
                            if response is not None:
                                print(response)






# client = OpenAI()
#
# audio_file = open("speech.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="text"
# )


