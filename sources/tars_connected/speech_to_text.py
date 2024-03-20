import speech_recognition
from tars_connected.text_to_response import TarsAnswering
# from neuralintents.assistants import BasicAssistant


class TarsCommandRecognizer:
    def __init__(self):
        # self.assistant = BasicAssistant("../intents.json", method_mappings={"print": self.print_un_truc})
        # self.assistant.fit_model(epochs=20)
        # self.assistant.save_model()
        self.tars_answerer = TarsAnswering()
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
            except speech_recognition.RequestError:
                print("wtf request error")

            except speech_recognition.UnknownValueError as e:
                print("No comprendo")
