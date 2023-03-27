import PySimpleGUI as sg
from recorder import Recorder

class recorderGUI:

    def open(self):
        layout = [
            [sg.Button("Record")],
            [sg.Text("Time: ",size= (5,1)), sg.InputText()],
            [sg.Button("Save Commercial")],
            [sg.Button("Save Content")],
            ]

        # Create the window
        window = sg.Window("Audio Capture", layout)
        recorder = Recorder()
        # Create an event loop
        while True:
            event, values = window.read()
            # End program if user closes window or
            if event == sg.WIN_CLOSED:
                recorder.stopRecording()
                break
            # presses the OK button
            elif event == "Record":
                #window.start_thread(lambda: recorder.startRecording(values[0]),('-THREAD-','-THREAD ENDED'))
                recorder.startRecording(values[0])
            elif event =="Save Commercial":
                recorder.stopRecording()
                recorder.saveCommercial()
            elif event =="Save Content":
                recorder.stopRecording()
                recorder.saveContent()

        window.close()

recorderGUI().open()

