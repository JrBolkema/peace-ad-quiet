import constants
import librosa

class AudioHelpers:
    def cut_audio(self,song):
        start = 0
        end = len(song)
        
        song_pieces = []

        while start + (constants.sample_rate * constants.seconds) < end:
            song_pieces.append(song[start:start+(constants.sample_rate * constants.seconds)])

            start += (constants.sample_rate * constants.seconds)
        return song_pieces

    def prepare_audio(self,song_path):
        list_matrices = []
        y,sr = librosa.load(song_path,sr=constants.sample_rate)

        song_pieces = self.cut_audio(y)
        for song_piece in song_pieces:
            melspect = librosa.feature.melspectrogram(y=song_piece,sr=sr)
            list_matrices.append(melspect)
        return list_matrices