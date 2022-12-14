import PySimpleGUI as sg
import polichinelos as pol
import modo




theme = sg.theme('reddit')

layout = [
    [sg.Image(filename='C:\\Users\\Usuario\\Desktop\\html\\Aula-Jonas\\reconhecedorDePolichinelos\\Contador_Polichinelos\\imagens\\healthy.png', )],
    [sg.Text('Seja bem vindo ao OPEN-TRAINER')],
    [sg.Button('Contador de polichinelos', key='polichinelos'), sg.Button('Contador de agachamentos', key='agachamento')],
    [sg.Button('Contador de rosca direta', key='rosca'), sg.Button('Contador de flexao', key='flexao')],
    [sg.Button('Verificar necessidades', key='verif')],
    [sg.Text('Modo'), sg.Combo(['Infinito', 'Personal'], key='modo', default_value= 'Infinito')]
    ]
    
window = sg.Window('Open-trainer', layout= layout)




while True:
    event, values = window.Read()

    modo.modo = values['modo']

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
            
    elif event == 'verif':
        sg.popup(pol.dataframe)
    else:
        sg.popup('Lamento, essa função ainda não está completa :(')

