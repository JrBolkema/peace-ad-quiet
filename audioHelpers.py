import numpy as np
import constants
import librosa

class AudioHelper:
    def cutAudio(self,song):
        start = 0
        end = len(song)
        
        songPieces = []

        while start + (constants.sample_rate * constants.seconds) < end:
            songPieces.append(song[start:start+(constants.sample_rate * constants.seconds)])

            start += (constants.sample_rate * constants.seconds)
        return songPieces

    def prepareAudio(self,song_path):
        list_matrices = []
        y,sr = librosa.load(song_path,sr=constants.sample_rate)
        songPieces = self.cutAudio(y)
        for songPiece in songPieces:
            melspect = librosa.feature.melspectrogram(y=songPiece,sr=sr)
            list_matrices.append(melspect)
        return list_matrices
    
    def prepareAudioForPrediction(self,rawAudio):
        data = rawAudio[:,0]
        return librosa.feature.melspectrogram(y=data,sr=constants.sample_rate)