import requests
import PySimpleGUI as sg
from downloader import check_update
from patcher import made_command


def status_online():
    try:
        requests.head("https://www.github.com", timeout=1)
        estatus = 'Online'
    except requests.ConnectionError:
        estatus = 'Offline'
    return estatus


def dialog_apk():
    file_path = sg.popup_get_file('Open APK file', file_types=(('apk file', '*.apk'),))
    return file_path


def main_gui():
    #Open file_dialog
    #DD
    applications = ['Youtube','Youtube Music', 'Tiktok','Twitch','Instagram','Other']    #List of applications that can be patched
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  
        [sg.Text('Simple Revanced-builder 1.3',justification='right', font=('Helvetica', 13),pad=((0, 0), (10, 0))),
         sg.Text(status_online(),pad=((220, 10), (10, 0)))],
        [sg.Text('Application: ',pad=((0, 0), (30, 0)), font=('Helvetica', 13)), 
         sg.Combo(values=applications, font=('Helvetica', 11), key='-dropdown-', size=(20, 5),pad=((5, 0), (30, 0)))],
        [sg.Button('Patch',key='-PATCH-',pad=((15, 0), (30, 0))),
         sg.Button('Check Update',enable_events=True,pad=((15, 0), (30, 0)),key='-Download-') ],
        ]
    
    window = sg.Window('Simple Revanced-builder', layout)

    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                break

            case '-Download-':
                check_update()

            case '-PATCH-':
                if not values['-dropdown-']:
                    sg.popup("Select an application to patch.")
                else:
                    file_path = dialog_apk()
                    if file_path:
                        made_command(file_path,values['-dropdown-'] )
                    else:   
                        sg.popup("Select the apk to patch")    
                    
    window.close()

main_gui()
