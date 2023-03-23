import PySimpleGUI as sg
from recorder import Recorder

layout = [
    [sg.Button("Record")],
    [sg.Text("Time: ",size= (5,1)), sg.InputText()],
    [sg.Button("Stop and Save")],]

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
        window.start_thread(lambda: recorder.startRecording(values[0]),('-THREAD-','-THREAD ENDED'))
    elif event =="Stop and Save":
        recorder.stopRecording()
        recorder.saveAudio()

window.close()



