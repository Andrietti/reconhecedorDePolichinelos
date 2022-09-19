from ast import Break
import PySimpleGUI as sg
import polichinelos as pol
import pygame




musica_tocando = True

theme = sg.theme('reddit')

layout = [
    [sg.Image(filename='C:\\Users\\Usuario\\Desktop\\html\\Aula-Jonas\\reconhecedorDePolichinelos\\Contador_Polichinelos\\imagens\\healthy.png', )],
    [sg.Text('Seja bem vindo ao OPEN-TRAINER')],
    [sg.Button('Contador de polichinelos', key='polichinelos'), sg.Button('Contador de agachamentos', key='agachamento')],
    [sg.Button('Contador de rosca direta', key='rosca')]
]
 
window = sg.Window('Open-trainer', layout= layout, element_padding=(10, 10))

while True:
    event, values = window.Read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'polichinelos':
        pol.polichinelos()
    elif event == 'agachamento':
        pol.agachamento()
    elif event == 'flexao':
        pol.flexao()
    elif event == 'rosca':
        pol.rosca_direta()
    else:
        sg.popup('Lamento, essa função ainda não está completa :(')

     