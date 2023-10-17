import os
from path_all import paths
import subprocess
import PySimpleGUI as sg

def patcher_def(input_apk,name_apk):
    tools_folder = paths()[1]
    patched_folder = paths()[2]
    tools_files = os.listdir(tools_folder)

    
    app_name = f'{name_apk}_Revanced.apk'
    output_apk = os.path.join(patched_folder,app_name)
    
            
    command = f'java -jar "{tools_folder}\{tools_files[0]}" patch -p -o "{output_apk}" -b "{tools_folder}\{tools_files[2]}"'\
        f' -m "{tools_folder}\{tools_files[1]}" "{input_apk}"'
    
    run_command_gui(command)


def run_command_gui(command):
    patched_folder = paths()[2]
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        layout = [
            [sg.Output(size=(60, 20), key='-OUTPUT-', pad=(0, 0))],
            [sg.Button('Cerrar'),sg.Button('Patched Folder',key='-PATCHEDFOLDER-',pad=((270, 0), (0, 0)))]
        ]
        
        window = sg.Window('Ejecutar Comando', layout, finalize=True)
        
        while True:
            event, _ = window.read(timeout=100)
            if event == 'Cerrar' or event == sg.WINDOW_CLOSED:
                process.terminate()
                break
                
            
            if event == '-PATCHEDFOLDER-':
                subprocess.run(['explorer',patched_folder ])

            output = process.stdout.readline()
            if output:
                window['-OUTPUT-'].print(output.strip())
        
        window['Cerrar'].update(disabled=True)
        window.close()
    
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        sg.popup_error('Error: ', error_output)


