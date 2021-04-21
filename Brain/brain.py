from transformers import pipeline, Conversation
from os import path

from Brain.memory.memory import Memory
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
        self.memory = Memory(path.abspath('Brain/memory/cell'))
        self.convo = dict({})
        self.hasVoice = False
    
    
    def feed(self, channel, message):
        try:
            conv = self.convo[channel]
            conv = my_convo(message)
            self.convo[channel] = conv
            self.memory.add_user_input(channel, str(message))
        except:
            self.convo[channel] = my_convo(message)
            
            
    def answer(self, channel):
        ans = self.pipeline([self.convo[channel]])
        self.memory.add_gen_response(channel, str(ans))
        print(self.convo)
        if self.hasVoice:
            return self.voice.speak(str(ans))
        else:
            return str(ans)
    
    def reset_memory(self, channel):
        conv = self.convo[channel]
        conv = my_convo('')
                
    def speak(self, sen):
        return self.voice(sen)
    
    def listen(self, audio):
        return self.voice(audio)

    def voiceModeOn(self):
        self.hasVoice = True
    
    def voiceModeOff(self):
        self.hasVoice = False
    