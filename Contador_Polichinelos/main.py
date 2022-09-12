from ast import Break
import PySimpleGUI as sg
import polichinelos as pol
import pygame

pygame.init() # iniciando o pygame
pygame.mixer.music.load('olhotigre.mp3') # Fazendo o pygame carregar uma música



musica_tocando = True

theme = sg.theme('reddit')

layout = [
    [sg.Image(filename='imagens\healthy.png', )],
    [sg.Text('Seja bem vindo ao OPEN-TRAINER')],
    [sg.Button('Contador de polichinelos', key='polichinelos'), sg.Button('Contador de agachamentos')],
    [sg.Button('Contador de flexões'), sg.Button('Contador de rosca direta')]
]

window = sg.Window('Open-trainer', layout= layout, element_padding=(10, 10))

while True:
    event, values = window.Read()

    if event == sg.WINDOW_CLOSED:
        break
    if event == 'polichinelos':
        pol.polichinelos()