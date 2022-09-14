import cv2                # Biblioteca para abrir a camera
import mediapipe as mp    # Biblioteca para a detecção de pontos de referência
import math               # Vai medir a distância entre os pontos
import pygame             # Importando o pygame para tocar uma musica
import keyboard

        


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
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)


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

    video = cv2.VideoCapture(0)

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
        draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = img.shape



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
            distQUADRIL = math.hypot(quDX - quEX, quDY - quEY)

            print(f'quadril: {distQUADRIL}')
            # maos <=150 pes >=150


            # Condicionais para verificar as distâncias descrevidas a cima
            # E verificar se os polichinelos foram executados com base
            # Na distância das mãos e dos pés
            if check == True and distMO <=150 and distPE >=150:
                contador +=1
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



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(img,(20,240),(280,120),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(img,texto,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)



        cv2.imshow('Resultado',img)
        cv2.waitKey(40)

def agachamento():

    video = cv2.VideoCapture('C:\\Users\\Usuario\\Desktop\\html\\Aula-Jonas\\reconhecedorDePolichinelos\\Contador_Polichinelos\\agachamento curto.mp4')

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
        draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = img.shape



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
            if check == True and distQUADRIL >= 470 and distPE >= 120:
                contador +=1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo

            if distQUADRIL < 400 and distPE >= 120:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(img,(20,240),(280,120),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(img,texto,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',img)
        cv2.waitKey(40)


def flexao():

    video = cv2.VideoCapture('C:\\Users\\Usuario\\Desktop\\html\\Aula-Jonas\\reconhecedorDePolichinelos\\Contador_Polichinelos\\flexao.mp4')

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
        draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = img.shape



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
            if check == True and omDY >= 730 and distCABECA <= 30:
                contador +=1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo

            if omDY <= 700 and distCABECA >= 40:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(img,(20,240),(280,120),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(img,texto,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',img)
        cv2.waitKey(40)


def rosca_direta():

    video = cv2.VideoCapture('C:\\Users\\Usuario\\Desktop\\html\\Aula-Jonas\\reconhecedorDePolichinelos\\Contador_Polichinelos\\rosca_direta.mp4')

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
        draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)


        # Extraindo as dimensões da imagem
        h,w,_ = img.shape



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
                contador +=1
                check = False # Alterando a variável check para falsa para não contar
                 # Mais de um polichinelo

            if distMODY >= distCOCXDY and distMOEY >= distCOCXEY:
                check = True # Quando o ultimo movimento é feito altera a variável para true
             # Para permitir que outro polichinelo seja finalizado e computado


        

            if keyboard.is_pressed('esc'): ### Caso esc seja pressionado, o código encerrará
                break           

            


            # Aqui, criamos o retangulo que vai armazenar o texto que diz quantos
            # Polichinelos o usuário fez

            texto = f'QTD {contador}'



            ### Função que cria a forma
            # De um retângulo no video
            cv2.rectangle(img,(20,240),(280,120),(255,0,0),-1)

            ### Função que cria a forma
            # De um retângulo no video

            # Função para adicionar um texto a área de informações	
            cv2.putText(img,texto,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)
            



        cv2.imshow('Resultado',img)
        cv2.waitKey(40)
