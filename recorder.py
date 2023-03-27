import soundcard as sc
import time
import numpy as np
from scipy.io.wavfile import write
import constants



class Recorder:
    speakers = sc.all_speakers()
    mics = sc.all_microphones(include_loopback=True)
    # get the current default microphone on your system:
    default_mic = mics[0]
    default_speaker = sc.default_speaker()

    data = []
    predictionData = []
    recording = False

    def listMicrophones(self):
        for i in range(len(self.mics)):
            try:
                print(f"{i}: {self.mics[i].name}")
            except Exception as e:
                print(e)
    
    def getRecordingForPrediction(self):
        with self.default_mic.recorder(samplerate=constants.sample_rate) as mic:
            data = mic.record(constants.sample_rate * constants.seconds)
            return data
        

    def startRecording(self,timeToRecord = 0):
        print("Recording Started")
        self.recording = True
        with self.default_mic.recorder(samplerate=constants.sample_rate) as mic:
            if timeToRecord == '':
                while self.recording:
                    self.data.extend(mic.record(constants.sample_rate))
            else:
                self.data.extend(mic.record(constants.sample_rate * int(timeToRecord)))
                self.stopRecording()
                self.saveUnclassified()

    def stopRecording(self):
        self.recording = False
        print("Recording Stopped")


    def saveContent(self):
        filepath = r'C:\Users\Jon\source\repos\peace-ad-quiet\content\\'
        self.saveAudio(filepath)

    def saveCommercial(self):
        filepath = r'C:\Users\Jon\source\repos\peace-ad-quiet\commercials\\'
        self.saveAudio(filepath)

    def saveUnclassified(self):
        filepath = r'C:\Users\Jon\source\repos\peace-ad-quiet\unclassified\\'
        self.saveAudio(filepath)

    def saveAudio(self,filePath):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestr}.wav"
        fullPath = filePath + filename

        scaled = np.int16(self.data / np.max(np.abs(self.data)) * 32767) 
        write(fullPath, constants.sample_rate, scaled)
        self.data = []
        print("File Saved")






        