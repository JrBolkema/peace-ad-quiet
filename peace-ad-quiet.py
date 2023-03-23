import soundcard as sc
import time
import numpy as np
from scipy.io.wavfile import write

speakers = sc.all_speakers()
mics = sc.all_microphones(include_loopback=True)
default_speaker = sc.default_speaker()
rate = 44100  # Record at 44100 samples per second
seconds = 3
# get the current default microphone on your system:
default_mic = mics[0]

# for i in range(len(mics)):
#     try:
#         print(f"{i}: {mics[i].name}")
#     except Exception as e:
#         print(e)

with default_mic.recorder(samplerate=rate) as mic, \
            default_speaker.player(samplerate=rate) as sp:
    #print("Recording...")
    data = mic.record(numframes=(rate * seconds))

    # print("Done! Pause your audio to hear the playback")
    # time.sleep(1)
    # sp.play(data)

timestr = time.strftime("%Y%m%d_%H%M%S")
filename = f"output_{timestr}.wav"
filepath = r'C:\Users\Jon\source\repos\peace-ad-quiet\commericals\\' + filename
scaled = np.int16(data / np.max(np.abs(data)) * 32767) 
write(filepath, rate, scaled)
print("File Saved!")

