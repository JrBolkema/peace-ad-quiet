import numpy as np
import os
import audioHelpers
import constants
from sklearn.model_selection import train_test_split
from tensorflow.python.keras import layers, models,optimizers


class ModelGenerator:
    repo_path = r'C:\Users\Jon\source\repos\peace-ad-quiet'
    all_audio = []
    classification = []
    currentDirectory = os.getcwd()

    def generateModel(self):
        self.getAndPrepareAudio()
        model = self.trainAndCompileModel()
        self.saveModel(model)

    def getAndPrepareAudio(self):
        audioHelper = audioHelpers.AudioHelpers()
        for file in os.listdir(self.currentDirectory + "\\commercials"):
            filename = os.fsdecode(file)
            if filename.endswith(".wav"):
                audio_pieces = audioHelper.prepare_audio(self.repo_path + "\\commercials\\" + filename)
                self.all_audio += audio_pieces
                self.classification += ([1]*len(audio_pieces))

        for file in os.listdir(self.currentDirectory + "\\content"):
            filename = os.fsdecode(file)
            if filename.endswith(".wav"):
                audio_pieces = audioHelper.prepare_audio(self.repo_path + "\\content\\" + filename)
                self.all_audio += audio_pieces
                self.classification += ([0]*len(audio_pieces))
    
    def trainAndCompileModel(self):
        x_train, x_test, y_train, y_test = train_test_split(np.array(self.all_audio), 
                                                            np.array(self.classification),
                                                            test_size=0.25,
                                                            random_state=42)

        x_val, x_test, y_val, y_test = train_test_split(x_test, 
                                                        y_test,
                                                        test_size=0.25,
                                                        random_state=42)
        # print(x_train.shape)
        input_shape=(128, 259,1)

        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1))

        model.compile(loss='binary_crossentropy',
                optimizer=optimizers.rmsprop_v2.RMSProp(learning_rate=0.001),
                metrics='accuracy')

        x_train = x_train.reshape(-1, 128, 259, 1)
        x_val = x_val.reshape(-1, 128, 259, 1)
        x_test = x_test.reshape(-1, 128, 259, 1)

        model.fit(x=x_train, y=y_train, epochs=5, validation_data=(x_val, y_val))

        return model

    def saveModel(self,model):
        model.save(constants.model_filename)