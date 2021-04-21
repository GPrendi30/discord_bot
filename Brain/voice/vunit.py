import os
from multiprocessing import Process
from python_on_whales import docker


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
    try:
        docker.run(TEXT_TO_SPEECH, detach= True, networks=['host'],name='Prophets-Voice')
        print("TTS started in port {}".format(TTS_PORT))
    except Exception as e:
        docker.start('Prophets-Voice')
        print("TTS Already running")
    
    
    
def init_stt():
    global SPEECH_TO_TEXT, STT_PORT
    try:
        docker.run(SPEECH_TO_TEXT, detach= True, publish=[(STT_PORT, 5000)], name='Prophets-Ears')
        print("STT started in port {}".format(STT_PORT))
    except:
        docker.start('Prophets-Ears')
        print('STT already running')
