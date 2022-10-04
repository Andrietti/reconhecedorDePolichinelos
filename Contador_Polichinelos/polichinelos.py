import cv2                # Biblioteca para abrir a camera
import mediapipe as mp    # Biblioteca para a detecção de pontos de referência
import math               # Vai medir a distância entre os pontos
import pygame             # Importando o pygame para tocar uma musica
import keyboard
import pandas as pd
import PySimpleGUI as sg
import modo as mn
import sqlite3 as sq

conexao = sq.connect('banco.db')

cursor = conexao.cursor()


conexao.execute('''CREATE TABLE IF NOT EXISTS exerc
                   (
                    Pol       INT,
                    Flex       INT,
                    Aga        INT,
                    Rosca       INT);''')

conexao.commit()

cursor.execute('''INSERT INTO exerc (Flex, Aga, Rosca, Pol)
VALUES (0, 0, 0, 0)''')

conexao.commit()


 
exercicios = {
        'exercício' : ['Polichinelos', 'Agachamento', 'Rosca_Direta', 'Flexão'],
        'repetições': [20, 20, 20 ,20]
    }

dataframe = pd.read_excel('df.xlsx')

        


video = cv2.VideoCapture(0) # Variável que armazena a função de captura de video,
#no caso, como passamos como parâmetro o índice zero, em vez de um caminho de video,
#irá fazer o video capture da webcam de índice 0 do nosso computador(no caso, a integrada)

# O mediapipe contém, uma espécie de rede neural própria
# chamando a biblioteca com o mp. o atributo solutions conecta ela a uma api do google
# dentro dessa api, podemos retirar as informações distribuídas por eles
# o atributo pose, é um tracking do corpo humano(Aquelas ligações e bolinhas la)
pose = mp.solutions.pose

# essa variável está armazeando a pose, passando como parâmetro
# o mínimo de semelhança entre os modelos previamente carregados
# e o video que será processado pela webcam.
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5, )


# A variável armazena o método que usamos para desenhar as linhas e pontos
# que vão fazer parte da composição do corpos identificados pelo noss
draw = mp.solutions.drawing_utils

# Contador para identificar quatos polichinelos foram feitos

# Essa variável só serve pra impedir o contador não contar mais de um polichinelo por vez
# Um video, não passa de um aglomerado de imagens sendo exibidas de forma rápida uma
# Atrás da outra, nós precisamos de uma variável que recebe True ou False, pois
# O laço de verificação do movimento, reconhecerá a mesma pose em diversas imagens
# E acrescentará um ao contador diversas vezes
# Após detectar que o movimento está certo uma vez, definos o valor de Check para False
# Desta maneira, como visto daqui a pouco, só fara a contagem uma vez




def polichinelos():

    

    if mn.modo == 'Personal':
        contador = dataframe['repetições'][0]
    else:
        contador = 0

    check = True
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (1280, 900))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)

            peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

            peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)

            peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)

            moDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)

            moDX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w)

            moEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)

            moEX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)

            quEY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)

            quEX = int(points.landmark[pose.PoseLandmark.LEFT_HIP].x*w)

            quDY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].y*h)

            quDX = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].x*w)


            
            


            # Função utilizada para extrair as cordenadas finais dos pés e mãos
            distMO = math.hypot(moDX-moEX,moDY-moEY) 
            distPE = math.hypot(peDX-peEX,peDY-peEY)
            distQUADRIL = math.hypot(quDY)

            print(f'quadril: {distQUADRIL}')
            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and distMO <=150 and distPE >=150:
                if mn.modo == 'Personal':
                    contador -=1
                    exercicios['repetições'][0] -= 1
                else:
                    contador +=1
                    exercicios['repetições'][0] -= 1
                
                
                check = False # Alterando a variável check para falsa para não contar
                # Mais de um polichinelo

            if distMO >150 and distPE <150:
                check = True # Quando o ultimo movimento é feito altera a variável para true
            # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'

            if distQUADRIL >= 600:
                texto = f'Se afaste um pouco'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(1200,800),(50,700),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(40,760),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)



        cv2.imshow('Resultado',novaimg)
        cv2.waitKey(40)
        
    cursor.execute('SELECT Pol FROM exerc')
    res = cursor.fetchone()[0]

    print(res)
            
    cursor.execute(f"""
    UPDATE exerc SET Pol = '{contador + res}'

    """)
    conexao.commit()

def agachamento():

    if mn.modo == 'Personal':
        contador = dataframe['repetições'][1]
    else:
        contador = 0
    check = True
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        novaimg = cv2.resize(img, (1280, 900))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)

            peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

            peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)

            peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)
            
            quEY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)
            
            


            # Função utilizada para extrair as cordenadas finais dos pés e mãos 
            distPE = math.hypot(peDX-peEX,peDY-peEY)
            distQUADRIL = math.hypot(quEY)

            print(f'quadril: {distQUADRIL}, pés {distPE}')
            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés


            if check and distQUADRIL >= 640 and distPE >= 250:
                if mn.modo == 'Personal':
                    contador -=1
                    exercicios['repetições'][1] -= 1
                else:
                    contador +=1
                    exercicios['repetições'][1] -= 1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo

            if distQUADRIL <= 540 and distPE >= 250:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'

            if distQUADRIL >= 660 and check == True:
                texto = f'Abaixe sua camera'



            ### Função que cria a forma
            # De um retângulo no video'
            cv2.rectangle(novaimg,(1200,800),(50,700),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(40,760),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        cv2.waitKey(40)

    cursor.execute('SELECT Aga FROM exerc')
    res = cursor.fetchone()[0]

    print(res)
            
    cursor.execute(f"""
    UPDATE exerc SET Aga = '{contador + res}'

    """)
    conexao.commit()


def flexao():


    if mn.modo == 'Personal':
        contador = dataframe['repetições'][3]
    else:
        contador = 0
    check = True
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (1280, 900))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)

            peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

            peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)

            peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)

            
            omDY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)
            
            cbEY = int(points.landmark[pose.PoseLandmark.LEFT_EAR].x*w)
            


            # Função utilizada para extrair as cordenadas finais dos pés e mãos 
            distPE = math.hypot(peDX-peEX,peDY-peEY)
            distOMBRO = math.hypot(omDY)
            distCABECA = math.hypot(cbEY)

            print(f'ombro: {distOMBRO} cabeça {distCABECA}')
            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and omDY >= 740 and distCABECA >= 840:
                if mn.modo == 'Personal':
                    contador -=1
                    exercicios['repetições'][3] -= 1
                    check = False
                else:
                    contador +=1
                    exercicios['repetições'][3] -= 1
                    check = False
        

            if omDY < 650 and distCABECA >= 840:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(1200,800),(50,700),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(40,760),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        cv2.waitKey(40)

    cursor.execute('SELECT Flex FROM exerc')
    res = cursor.fetchone()[0]

    print(res)
            
    cursor.execute(f"""
    UPDATE exerc SET Flex = '{contador + res}'

    """)
    conexao.commit()


def rosca_direta():

    if mn.modo == 'Personal':
        contador = dataframe['repetições'][2]
    else:
        contador = 0
    check = True
    
    while True: # Loop para rodar o video
        


        # Variáveis que vão receber o que é reconhecido pela webcam
        # !!! A primeira é apenas um teste, para verificar se ela está aberta ou não
        success,img = video.read()


        # A variável videoRGB recebe o video com a função cvtColor aplicada nele
        # Essa função tem a capacidade de alterar o padrão de cores do video/imagem
        # O opencv Não usa o padrão RGB, então normalmente essa função é usada para
        # A conversão de uma imagem opencv2 para uma imagem RGB
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        novaimg = cv2.resize(img, (1280, 900))


        # Essa variável vai armazenar o resultado do processamento do nosso video
        # Após o computador verificar se realmente existe um corpo no video
        # Vai fazer a ligação entre os pontos que estão configurados na rede neural
        # Devemos notar que para este código, não precisamos baixar nenhuma rede neural
        # Previamente, pois a biblioteca media pipe faz uma ligação com a api do google
        # Que devolve as informações necessárias para o funcionamento do código
        results = Pose.process(videoRGB)

        # A variável points vai armazenar o atributo pose_landmarks 
        # do objeto, ou variável results, no caso, aqueles pontinhos que marcam cada região
        # do corpo
        points = results.pose_landmarks

        # Esse método nós usamos para desenhar as ligações entre os pontos
        # Armazenados na variável points
        draw.draw_landmarks(novaimg,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = novaimg.shape



        if points: # condição que vai verificar se a variavel points não está vazia
            # caso a variável esteja vazia ele não tentará encontrar os pontos


            # Coordenadas de cada ponto dos pés e mãos
            
            omDY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)
        
            omEY = int(points.landmark[pose.PoseLandmark.LEFT_SHOULDER].y*h)

            moDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)

            moEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)

            cocxDY = int(points.landmark[pose.PoseLandmark.RIGHT_HIP].y*h)

            cocxEY = int(points.landmark[pose.PoseLandmark.LEFT_HIP].y*h)

    
            
            

        


            # Função utilizada para extrair as cordenadas finais dos pés e mãos 
            distOMBROD = math.hypot(omDY)
            distOMBROE = math.hypot(omEY)
            distMODY = math.hypot(moDY)
            distMOEY = math.hypot(moEY)
            distCOCXDY = math.hypot(cocxDY)
            distCOCXEY = math.hypot(cocxEY)

            print(f'mãos {distMODY}, {distMOEY} ombros {distOMBROD}, {distOMBROE}')
            

            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and distMODY <= distOMBROD and distMOEY <= distOMBROE:
                if mn.modo == 'Personal':
                    contador -= 1
                else:
                    contador += 1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo

            if distMODY >= distCOCXDY and distMOEY >= distCOCXEY:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


            if contador == 0:
                if mn.modo == 'Personal':
                    sg.popup('Parabéns, você terminou suas repetições')
                    break
                

        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(novaimg,(1200,800),(50,700),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(novaimg,texto,(40,760),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',novaimg)
        cv2.waitKey(40)

    cursor.execute('SELECT Rosca FROM exerc')
    res = cursor.fetchone()[0]

    print(res)
            
    cursor.execute(f"""
    UPDATE exerc SET Rosca = '{contador + res}'

    """)
    conexao.commit()

