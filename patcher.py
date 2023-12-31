import os
import shutil
import subprocess
import threading
import PySimpleGUI as sg
from pathlib import Path


def paths():
    revanced_folder = Path(os.environ["USERPROFILE"]) / "Documents" / "Simple Revanced"
    tools_folder = revanced_folder / "Tools"
    patched_folder = revanced_folder/ "Patched APK"
    folders = [revanced_folder,tools_folder,patched_folder]
    return folders


def made_command(input_apk,name_app):
    #Get Paths folders
    tools_folder = paths()[1]
    patched_folder = paths()[2]
    tools_files = os.listdir(tools_folder) #Revanced tools files
    #APK NAME
    number_apk = 0
    output_apk = Path(patched_folder) / f'{name_app}_Revanced_{number_apk}.apk'

    while output_apk.exists():
        number_apk += 1
        output_apk = Path(patched_folder) / f'{name_app}_Revanced_{number_apk}.apk'

    #COMMAND
    match name_app:
        case 'Youtube':
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' --include "Custom branding" -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')

        case 'Youtube Music':
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')

        case 'Tiktok':
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')

        case 'Twitch':
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')
        
        case 'Instagram':
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')

        case _:
            command = (f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'
            + f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"')
    #print(command)
    run_command_gui(command)


def run_command_gui(command):
    #I made this with chat-gpt to be honest, no really understand how it works.(just: run_command_gui)
    patched_folder = paths()[2]
    
    def execute_command():
        nonlocal window
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output:
                window['-OUTPUT-'].print(output.strip())
            else:
                break
        
        window['Close'].update()
        process.terminate()
    
    try:
        threading.Thread(target=execute_command, daemon=True).start()
        layout = [
            [sg.Output(size=(60, 20), key='-OUTPUT-', pad=(0, 0))],
            [sg.Button('Close'), sg.Button('Patched Folder', key='-PATCHEDFOLDER-', pad=((270, 0), (0, 0)))]
        ]
        window = sg.Window('Commmand', layout, finalize=True)
        while True:
            event, _ = window.read()
            if event == 'Close' or event == sg.WINDOW_CLOSED:
                delete_cache()
                break
            if event == '-PATCHEDFOLDER-':
                subprocess.run(['explorer', patched_folder])
        window['Close'].update(disabled=True)
        window.close()
        
    except subprocess.CalledProcessError as e:
        sg.popup_error('Error: ', e.stderr)


def delete_cache():
    #Delete cache-files 
    patched_folder = paths()[2]
    for cache in os.listdir(patched_folder):
        if cache.endswith(".keystore") or cache.endswith(".json"):
            file = Path(patched_folder / cache)
            os.remove(file)
        elif cache.endswith("-resource-cache"):
            file = Path(patched_folder / cache)
            shutil.rmtree(file)#Shutil to delete folder because when a folder has files os.remove is dumb

