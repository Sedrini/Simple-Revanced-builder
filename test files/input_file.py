import PySimpleGUI as sg

sg.theme('Dark Red')

layout = [[sg.Text('Browse to a file')],
          [sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse()]]

event, values = sg.Window('File Compare', layout).read(close=True)

print(f'You chose: {values["-FILE-"]}')