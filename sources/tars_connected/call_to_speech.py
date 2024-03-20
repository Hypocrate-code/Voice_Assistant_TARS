import pvporcupine
import pyaudio
import struct
from tars_connected.speech_to_text import TarsCommandRecognizer
from tars_connected.response_to_speech import TarsSpeaker
import winsound
class TarsVocall:
    def __init__(self):
        self.tars_recognizer = TarsCommandRecognizer()
        self.tars_vocal = TarsSpeaker()
        kw_path = ["tars_connected/win.ppn"]
        porc = pvporcupine.create(access_key="2iyFmGQrWF1FqHFWn3yf9UIJs2tD0uGT0Tix8JgvMILfcBwTUxMKUA==", keyword_paths=kw_path, model_path="tars_connected/porcupine_params_fr.pv", sensitivities=[0.6])
        pa = pyaudio.PyAudio()
        audio = pa.open(
            rate=porc.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porc.frame_length
        )
        while True:
            pcm = audio.read(porc.frame_length)
            pcm = struct.unpack_from("h" * porc.frame_length, pcm)
            keyword_index = porc.process(pcm)
            if keyword_index >= 0:
                winsound.Beep(640, 700)
                print("Parlez...")
                self.tars_recognizer.recognize()
