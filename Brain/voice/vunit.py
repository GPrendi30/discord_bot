import os
from multiprocessing import Process

TEXT_TO_SPEECH="gprendi30/voice"
SPEECH_TO_TEXT="quay.io/codait/max-speech-to-text-converter"

TTS_PORT=5002
STT_PORT=5000



def init_voice():
    # initializing processes
    TTS_Process = Process(target=init_tts)

    # initializing processes
    STT_Process = Process(target=init_stt)
    
    # starting processes
    try:
        TTS_Process.start()
        STT_Process.start()

    except:
        print("Processes already started")
      
def init_tts():
    global TEXT_TO_SPEECH, TTS_PORT
    os.system('docker run -d {} {}'.format("--network=host", TEXT_TO_SPEECH))
    
    print("TTS started in port {}".format(TTS_PORT))
    
    
def init_stt():
    global SPEECH_TO_TEXT, STT_PORT
    os.system('docker run -d {} {}'.format("-p 5000:5000", SPEECH_TO_TEXT))
    
    print("STT started in port {}".format(STT_PORT))
    