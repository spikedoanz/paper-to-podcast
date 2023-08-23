from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
import numpy as np
import json
import re
# download and load all models

# generate audio from text


#testing stuff
def create_recording(logpath, recordingpath, conversation_count = 0):
    preload_models()
    # Change out speakers here
    with open (logpath, "r") as f:
        if conversation_count == 0:
            data = json.load(f)['record']
        else:   
            data = json.load(f)['record'][:conversation_count]

    audio_array = []
    for i in range(len(data)):
        text = data[i]['content']
        role = data[i]['role']
        if role == 'user':
            voice = "v2/en_speaker_2"
        else:
            voice = "v2/en_speaker_6"
        sentences = re.split(r'[.!?]', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        for _ in sentences:
            audio_array.extend(generate_audio(_, history_prompt=voice))
        print(text)
    #recordingspath = "./recordings/" + time + ".wav" 
    recording_data= np.array(audio_array)
    write_wav(recordingpath, SAMPLE_RATE, recording_data)
if __name__ == "__main__":
    logpath = "/home/tama/work/pdf-podcast/examples/21:25-18-08-2023.json"
    recording_directory = "./recordings/"
    recording_name = 'test.wav'
    recordingpath = recording_directory + recording_name
    create_recording(logpath, recordingpath)