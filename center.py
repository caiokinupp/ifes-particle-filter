#Ajuda na passagem de argumentos para o programa
import argparse

#Ferramentas criadas usando OpenCV
import imutils

#importando o OpenCV
import cv2

import particle_filter as pf
import pf_tools as pft
import time

#Construindo a estrutura de argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())


#Fronteiras do espectro de cor no modelo HSV
corLower = (29, 86, 6)
corUpper = (64, 255, 255)

#Lendo o video com OpenCV
video  = cv2.VideoCapture(args["video"])

#Inicializando o filtro de particulas
lst_particulas = pft.initialize_pf((1277,399))

while True:
    #calculando o tempo para processar um frame
    start = time.time()

    #Captura o frame atual
    cap, frame = video.read()

    #Verifica se esta no final do Video
    if frame is None:
        break

    #Reduz o tamanho do frame para reduzir a carga de processamento
    #frame = imutils.resize(frame, width=1000) #600px

    #Borra a imagem para reduzir os ruidos e deixa-la uniforme
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    #Converte o frame para o modelo de cor HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #Aplica uma mascara limitada pelas fronteiras, tornando o frame binario
    mask = cv2.inRange(hsv, corLower, corUpper)

    #Reduzindo as imperfeicoes removendo "bolhas" e "erosoes" do frame
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    #Identificando o contorno na mascara
    contorno = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Garantir que vai ser compativel com opencv 2.4 e 3
    contorno = contorno[0] if imutils.is_cv2() else contorno[1]

    #Inicializar as coordenadas do centro
    center = None

    #Verificando se pelo menos um contorno foi identificado
    if len(contorno) > 0:

        #Identificando o maior contorno
        c = max(contorno, key=cv2.contourArea)

        #Identifica o menor delimitador
        ((x, y), raio) = cv2.minEnclosingCircle(c)

        #Identificando coordenadas do centro
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #Aplicando o filtro de particulas com relacao ao centro
        lst_particulas = pf.filtro_de_particulas(center,lst_particulas)

        #Printando cada particula
        for part in lst_particulas:
            cv2.circle(frame, (int(part.pos_x),int(part.pos_y)), 5, (0, 255, 255), 2)

        if raio > 10:
            #Printando o circulo calculado pela média das partículas
            cv2.circle(frame, pft.media_pos(lst_particulas), int(raio),(0, 255, 255), 2)
            #Printando a centroid obtida pelo OpenCV
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        #Exibindo o frame de saída
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        #Se apertar a tecla "q", interrompe o Loop
        if key == ord("q"):
            break
    #calculando o tempo para processar um frame
    end = time.time()

#fechar video e janelas
video.release()
cv2.destroyAllWindows()
