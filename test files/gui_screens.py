import PySimpleGUI as sg

layout1 = [[sg.Text('Pantalla 1'), sg.Button('Ir a Pantalla 2')]]
layout2 = [[sg.Text('Pantalla 2'), sg.Button('Ir a Pantalla 1')]]
layout_actual = layout1

window = sg.Window('Ventana de Pantallas', layout_actual)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ir a Pantalla 2':
        window['_CONTAINER_'].update(layout2)  # Utiliza window[key] para acceder al elemento
        layout_actual = layout2
    if event == 'Ir a Pantalla 1':
        window['_CONTAINER_'].update(layout1)  # Utiliza window[key] para acceder al elemento
        layout_actual = layout1

window.close()
