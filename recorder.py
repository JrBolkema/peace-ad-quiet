import soundcard as sc
import time
import numpy as np
from scipy.io.wavfile import write
import random



class Recorder:
    # speakers = sc.all_speakers()
    mics = sc.all_microphones(include_loopback=True)
    # get the current default microphone on your system:
    default_mic = mics[0]
    default_speaker = sc.default_speaker()
    
    rate = 44100  # Record at 44100 samples per second
    seconds = 3
    data = []
    recording = False

    def listMicrophones(self):
        for i in range(len(self.mics)):
            try:
                print(f"{i}: {self.mics[i].name}")
            except Exception as e:
                print(e)

    def startRecording(self,timeToRecord = 0):
        print("Recording Started")
        self.recording = True
        with self.default_mic.recorder(samplerate=self.rate) as mic:
            if timeToRecord == '':
                while self.recording:
                    self.data.extend(mic.record(self.rate))
            else:
                self.data.extend(mic.record(self.rate * int(timeToRecord)))
                self.stopRecording()
                self.saveAudio()

    def stopRecording(self):
        self.recording = False
        print("Recording Stopped")

    def saveAudio(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestr}.wav"
        filepath = r'C:\Users\Jon\source\repos\peace-ad-quiet\commericals\\' + filename

        scaled = np.int16(self.data / np.max(np.abs(self.data)) * 32767) 
        write(filepath, self.rate, scaled)
        self.data = []
        print("File Saved")






        