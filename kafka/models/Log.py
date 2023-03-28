import platform
import time


class Log:
    def __init__(self,confidence):
        self.SampleConfidence = confidence
        self.Timestamp = time.time()
        self.OperatingSystem = platform.platform()