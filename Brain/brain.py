from transformers import pipeline, Conversation

from Brain.voice.voice import Voice

class my_convo(Conversation):
    
    def __repr__(self):
        output = self.generated_responses[-1]
        return output
        

class Brain:
    ''' Brain of the Bot '''
    def __init__(self):
        self.pipeline = pipeline("conversational")
        self.voice = Voice()
        self.convo = None
        self.hasVoice = False
    
    
    def feed(self, message):
        self.convo = my_convo(message)
    
            
    def answer(self):
        ans = self.pipeline([self.convo])
        
        if self.hasVoice:
            return self.voice.speak(str(ans))
        else:
            return str(ans)
    
                
    def speak(self, sen):
        return self.voice(sen)
    
    def listen(self, audio):
        return self.voice(audio)

    def voiceModeOn(self):
        self.hasVoice = True
    
    def voiceModeOff(self):
        self.hasVoice = False
        
        

