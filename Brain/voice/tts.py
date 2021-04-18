import requests
import os
import sounddevice as sd
from scipy.io.wavfile import write
import json

def text_to_speech(text, filename):  
    try:
        os.remove(filename)
    except:
        pass
     
    txt = ""
    for t in text:
        if t.isalnum():
            txt += t
        else:
            t = t.encode('utf-8')
            txt += "%" + t.hex().upper()
              
    resp = requests.get("http://localhost:5002/api/tts?text={}".format(txt))
    with open(filename, mode='bx') as f:
        f.write(resp.content)

    return filename


def speech_to_text(audio):              
    resp = requests.post("http://localhost:5000/model/predict", files={'audio': open(audio, 'rb')})
    resp = json.loads(resp.content)
    
    print(resp)
    try: 
        return resp['prediction']
    except:
        return ""


def record():
    fs = 22100  # Sample rate
    seconds = 3  # Duration of recording
    print('Recording.')
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print('Recording..')
    
    write('output.wav', fs, myrecording)  # Save as WAV file \
    print('Done recording.')
    return 'output.wav'
