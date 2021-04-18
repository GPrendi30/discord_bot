from Brain.voice.vunit import init_voice
from Brain.voice.tts import text_to_speech, speech_to_text


class Voice:
    
    def __init__(self):
        init_voice()
        
    def speak(self, sen):
        return text_to_speech(sen, "ans.wav")
    
    def listen(self, audio):
        return speech_to_text(audio)      