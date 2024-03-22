import speech_recognition
from tars_connected.text_to_response import TarsAnswering
from tars_connected.tars_functions import FunctionRecognizer
from tars_connected.utils import make_sound
class TarsCommandRecognizer:
    def __init__(self):
        self.tars_answerer = TarsAnswering()
        self.function_recognizer = FunctionRecognizer(self.tars_answerer.tars_vocal)
        self.recognizer = speech_recognition.Recognizer()  # Initialiser Speech Recognition
        with speech_recognition.Microphone() as mic:  # Avec le microphone par défaut
            self.recognizer.adjust_for_ambient_noise(mic, duration=.5)

    def recognize(self):
        with speech_recognition.Microphone() as mic:  # Avec le microphone par défaut
            self.recognizer.adjust_for_ambient_noise(mic, duration=.5)
            try:
                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                if not self.function_recognizer.recognize_functions(text.lower()):
                    make_sound("tars_connected/high_bip.mov")
                    self.tars_answerer.answer(text)
            except speech_recognition.RequestError:
                make_sound("tars_connected/bug_bip.m4a")

            except speech_recognition.UnknownValueError as e:
                make_sound("tars_connected/bug_bip.m4a")
