import os
import time

import numpy as np
import constants
from modelGenerator import ModelGenerator
from audioHelpers import AudioHelper
from keras.models import load_model
from recorder import Recorder
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL,COMObject
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume,IAudioEndpointVolume,IAudioEndpointVolumeCallback




def main():
    print("Hello World!")

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    audioHelper = AudioHelper()
    if not os.path.exists(constants.model_filename):
        generator = ModelGenerator()
        model = generator.generateModel()
        print("Generated new model.")
    else:
        model = load_model(constants.model_filename)
        print("Loaded model from disk.")
    

    while True:
        print("Taking Sample...")
        recorder = Recorder()
        audio = recorder.getRecordingForPrediction()

        normalizedAudio = audioHelper.prepareAudioForPrediction(audio)
        normalizedAudio = normalizedAudio.reshape(-1, 128, 259, 1)
        result = model.predict(normalizedAudio,verbose=0)
        print(result[0][0])

        if(result[0][0] < 2): # probably no audio, don't poll again
            time.sleep(constants.seconds)
        elif result[0][0] > 150: # is not commercial
            print("Unmute")
            volume.SetMute(0, None)
        else: 
            print("Mute")
            volume.SetMute(1, None)

main()

