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
from kafka.peaceAdQuietProducer import Producer
from kafka.models.Log import Log




def main():
    print("Hello World!")

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    audioHelper = AudioHelper()
    recorder = Recorder()
    producer = Producer()
    if not os.path.exists(constants.model_filename):
        generator = ModelGenerator()
        model = generator.generateModel()
        print("Generated new model.")
    else:
        model = load_model(constants.model_filename)
        print("Loaded model from disk.")
    

    while True:
        print("\nTaking Sample...")
        audio = recorder.getRecordingForPrediction()

        normalizedAudio = audioHelper.prepareAudioForPrediction(audio)
        normalizedAudio = normalizedAudio.reshape(-1, 128, 259, 1)
        result = model.predict(normalizedAudio,verbose=0)
        confidence = result[0][0]

        print(f'Confidence: {confidence}')

        kafkaSchema = Log(confidence = confidence)

        if(confidence < 2): # probably no audio, don't poll again
            print("No Audio Detected. Pausing.")

            time.sleep(constants.seconds)
        elif confidence > 150: # is not commercial
            handleUnmute(volume,producer,kafkaSchema)
        else: 
            handleMute(volume,producer,kafkaSchema)

def handleMute(volume, producer, kafkaSchema):
    print("Muting...")
    volume.SetMute(1, None)
    # create class and schema for values
    producer.produceMuteLog("",kafkaSchema)

def handleUnmute(volume, producer, kafkaSchema):
    print("Unmuting...")
    volume.SetMute(0, None)
    # create class and schema for values
    producer.produceUnmuteLog("", kafkaSchema)

main()

