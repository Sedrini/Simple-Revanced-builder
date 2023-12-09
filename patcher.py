import os
import shutil
from path_all import paths
import subprocess
import PySimpleGUI as sg
from pathlib import Path
import threading


def patcher_def(input_apk,name_apk):
    tools_folder = paths()[1]
    patched_folder = paths()[2]
    tools_files = os.listdir(tools_folder)
    #APK NAME
    apk_number = 0
    app_name = f'{name_apk}_Revanced_'+str(apk_number)+".apk"
    output_apk = Path(os.path.join(patched_folder,app_name))
    #Check if file exist to modify the name
    while output_apk.is_file():
        apk_number += 1
        app_name = f'{name_apk}_Revanced_'+str(apk_number)+".apk"
        output_apk = Path(os.path.join(patched_folder,app_name))
    #COMMAND
    options = {
    "Youtube": lambda: f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}" --include "Custom branding"'\
        f' -m "{tools_folder}\{tools_files[1]}"   "{input_apk}"'}
    default_command = f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'\
        f' -m "{tools_folder}\{tools_files[1]}"  "{input_apk}"'
    command = options.get(name_apk, lambda: default_command)()
    #print(command)
    run_command_gui(command)

def run_command_gui(command):
    patched_folder = paths()[2]
    
    def execute_command():
        nonlocal window
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output:
                window['-OUTPUT-'].print(output.strip())
            else:
                delete_cache()
                break
        
        window['Close'].update()
        delete_cache()
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
                break
            if event == '-PATCHEDFOLDER-':
                subprocess.run(['explorer', patched_folder])
        window['Close'].update(disabled=True)
        window.close()
        
    except subprocess.CalledProcessError as e:
        sg.popup_error('Error: ', e.stderr)

def delete_cache():
    patched_folder = paths()[2]
    for cache in os.listdir(patched_folder):
        if cache.endswith(".keystore") or cache.endswith(".json"):
            file = Path(os.path.join(patched_folder,cache))
            os.remove(file)
        elif cache.endswith("-resource-cache"):
            file = Path(os.path.join(patched_folder,cache))
            shutil.rmtree(file)#Shutil to delete folder because when a folder has files os.remove is dumb
        else:
            None