import speech_recognition
from tars_connected.text_to_response import Tars_answering
# from neuralintents.assistants import BasicAssistant
import winsound

class Tars_command_recognizer:
    def __init__(self):
        # self.assistant = BasicAssistant("../intents.json", method_mappings={"print": self.print_un_truc})
        # self.assistant.fit_model(epochs=20)
        # self.assistant.save_model()
        self.tars_answerer = Tars_answering()
        self.recognizer = speech_recognition.Recognizer()  # Initialiser Speech Recognition
        with speech_recognition.Microphone() as mic:  # Avec le microphone par défaut
            self.recognizer.adjust_for_ambient_noise(mic, duration=.5)

    def recognize(self):
        with speech_recognition.Microphone() as mic:  # Avec le microphone par défaut
            self.recognizer.adjust_for_ambient_noise(mic, duration=.5)
            try:
                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                print(text)
                self.tars_answerer.answer(text)
                    #
                    # elif self.mots_activation[0] in text or self.mots_activation[1] in text or self.mots_activation[2] in text or self.mots_activation[3] in text:
                    #     while True:
                    #         print("J'écoute ?...")
                    #         try:
                    #             audio = self.recognizer.listen(mic)           # Ecoute jusqu'à ce qu'il détecte un vide
                    #             text = self.recognizer.recognize_google(audio, language="fr-FR")
                    #             text = text.lower()
                    #
                    #             if text in self.mots_de_fin:
                    #                 print("Au revoir !")
                    #                 return
                    #             else:
                    #                 print(f"\nVotre question: {text}\n")
                    #                 self.tars.answer(text)
                    #                 break
                    #         except speech_recognition.RequestError:
                    #             print(">>>> Error: API was unreachable or unresponsive")          # API was unreachable or unresponsive
                    #             print(">>>> Problème de connexion avec l'API")

                    # except speech_recognition.UnknownValueError:
                    #     print(">>>> Pardon, veuillez répéter")

            except speech_recognition.RequestError:
                pass

            except speech_recognition.UnknownValueError as e:
                winsound.Beep(440, 700)

# client = OpenAI()
#
# audio_file = open("speech.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1",
#   file=audio_file,
#   response_format="text"
# )
