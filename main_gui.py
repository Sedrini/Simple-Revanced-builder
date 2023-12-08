import PySimpleGUI as sg
import os
import requests
import win32api
from path_all import paths
from downloader import check_update
from patcher import patcher_def

def check_folders(): #NOT IN USE, BUT INCASE THE OTHER FAILS
    folders = paths()
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            file_path = folder / "my_file.txt"
            if os.path.exists(file_path):
                win32api.SetFileAttributes(str(file_path), win32api.FILE_ATTRIBUTE_NORMAL)

def status_online():
    try:
        requests.head("https://www.github.com", timeout=1)
        # Do something
        estatus = 'Online'
    except requests.ConnectionError:
        # Do something
        estatus = 'Offline'
    return estatus

def main_gui():
    applications = ['Youtube','Youtube Music', 'Tiktok','Twitch','Instagram','Other']    #List of applications that can be patched
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  
        [sg.Text('Simple Revanced-builder 1.2',justification='right', font=('Helvetica', 13),pad=((0, 0), (10, 0))),
         sg.Text(status_online(),pad=((220, 10), (10, 0)))],
        [sg.Text('Application: ',pad=((0, 0), (30, 0)), font=('Helvetica', 13)), 
         sg.Combo(values=applications, font=('Helvetica', 11), key='-dropdown-', size=(20, 5),pad=((5, 0), (30, 0)))],
        [sg.Button('Patch',key='-PATCH-',pad=((15, 0), (30, 0))),
         sg.Button('Download Files',enable_events=True,pad=((15, 0), (30, 0)),key='-Download-') ],
        ]

    # Create the Window
    window = sg.Window('Simple Revanced-builder', layout)
    # Event Loop to process "events" and get the "values" of the inputs

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        
        if event == '-Download-':
            check_update()
 
        if event == '-PATCH-':
            file_path = sg.popup_get_file('Open APK file', file_types=(("APK FILE", "*.apk"),))
            if values['-dropdown-'] == "":
                sg.popup_get_text("Explain your feelings that led you to make this decision.")   
            else:
                file_path
                if file_path != None :
                    print(file_path)
                    patcher_def(file_path,values['-dropdown-'] )     
                else:
                    sg.popup_get_text("Explain your feelings that led you to make this decision.")   
                    None

                
        

    window.close()

main_gui()