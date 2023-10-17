import PySimpleGUI as sg
import subprocess

def run_command_gui(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        layout = [
            [sg.Output(size=(60, 20), key='-OUTPUT-', pad=(0, 0))],
            [sg.Button('Cerrar'),sg.Button('Patched Folder',key='-PATCHEDFOLDER-')]
        ]
        
        window = sg.Window('Ejecutar Comando', layout, finalize=True)
        
        while True:
            event, _ = window.read(timeout=100)
            if event == 'Cerrar' or event == sg.WINDOW_CLOSED:
                process.terminate()
                break
                
            
            if event == '-PATCHEDFOLDER-':
                subprocess.run(['explorer', ])

            output = process.stdout.readline()
            if output:
                window['-OUTPUT-'].print(output.strip())
        
        window['Cerrar'].update(disabled=True)
        window.close()
    
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        sg.popup_error('Error al ejecutar el comando', error_output)

run_command_gui('ping google.com')
