#Esse arquivo guarda as funções que serão executadas usando os frames capturados pela câmera

#Importando dependencias
from matplotlib import pyplot as plt
import  cv2
import numpy as np
import imutils
import time as t
import easyocr
from tkinter import END
from keras.models import load_model
import os

#Inicializando as variáveis de controle

#Controle de vagas
ocupado1 = False
ocupado2 = False
ocupado3 = False
ocupado4 = False
ocupado5 = False
ocupado6 = False

#Controle do frame de mudança de estado das vagas
framecount = 0
framevaga1 = 0
framevaga2 = 0
framevaga3 = 0
framevaga4 = 0
framevaga5 = 0
framevaga6 = 0

#Controle se placa foi detectada
placa_detec = False

#Controle se placa foi localizada
placa_localizada = False

#Controle se efetuou leitura da placa com sucesso
placa = None

#Pegando pasta do app
pastaApp = os.path.dirname(__file__)

#Pathing do modelo de ml
pathModelo = pastaApp + "//keras_model//keras_model.h5"

#Pathing dos labels do modelo
pathLabel = pastaApp + "//keras_model//labels.txt"

#Inicilização do modelo de ml
model = load_model(pathModelo)

#Leitura dos labels do ml
labels = open(pathLabel, 'r').readlines()

#Setando linguagem do easyocr para inglês
reader = easyocr.Reader(['en'])

#Setando números e letras aceitas
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


#### FUNÇÕES

#Essa função é a de reconhecimento de placa
def camPlaca(frame, interface):
    #Declaração das variáveis a ser usadas
    global placa_detec
    global placa_localizada
    global framecount
    global placa
    global model
    global labels
    global reader
    global nums
    global letters
    
    #Mudando tamanho da imagem para usar no ml
    image = cv2.resize(frame.copy(), (224, 224), interpolation=cv2.INTER_AREA)

    #Transformando a imagem em nparray
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    
    #Normalizando a imagem
    image = (image / 127.5) - 1
    
    #Efetuando predição do modelo na imagem
    probabilities = model.predict(image, verbose = 0)
    
    #Pegando a maior probabilidade da predição do modelo
    obj = labels[np.argmax(probabilities)]
    
    #Checando se a maior probabilidade é de ter uma placa ou não, se tiver declara variável placa_detec como True
    if obj[0] == "0":
        placa_detec = True

        #Zera contagem de frames que uma placa foi detectada
        framecount = 0
    else:
        placa_detec = False

    #Se placa_detec é True
    if placa_detec:

        #Criando uma roi para trabalhar em cima dela
        roi = frame

        #Aplicando filtro cinza
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        #Aplicando filtro bilateral para redução de ruídos
        bFilter = cv2.bilateralFilter(gray, 11, 17, 17)
        
        #Aplicando filtro Canny para destacar as bordas
        edged = cv2.Canny(bFilter, 30, 200)

        #Mostrando o frame com os filtros aplicados
        cv2.imshow("gray", edged)

        #Achando contornos na imagem, ordenando em ordem decrescente pela área do contorno e pegando somente os 10 primeiros contornos
        contours = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        #Inicilizando variável location que será usado para guardar a localização da placa
        location = None

        #Iterando cada contorno dentro da lista de contornos
        for cnt in contours:
            #Pegando perímeto do contorno
            peri = cv2.arcLength(cnt, True)

            #Usando o perímetro e multiplicando por 0.018 para fechar contornos e aproximar de um polígono
            approx = cv2.approxPolyDP(cnt, 0.018 * peri, True)

            #Se o contorno tem 4 arestas é porque é um quadrilátero
            if len(approx) == 4:

                #Pegando as medidas do retangulo que o contorno forma
                (x, y, lar, alt) = cv2.boundingRect(cnt)

                #Pegando relação largura e altura
                proporc = lar/alt

                #Se a relação larg/alt for maior que 1 é um retangulo que tem mais largura que altura
                if proporc > 1:

                    #Pegando área do retangulo
                    area = lar*alt

                    #Se área for maior que 10000 é um objeto de tamanho considerável (reduzindo ruídos e falso positivos)
                    if area > 10000:

                        #Passado todos esses filtros é bem provável que tenhamos chegado na placa
                        #Desenhando um retangulo verde em volta da placa
                        cv2.rectangle(roi, (x, y), (x+lar, y+alt), (0, 255, 0), 2)
                        
                        #Setando a localização da placa
                        location = approx

                        #Variável de controle placa_localizada é setado para True
                        placa_localizada = True

                        #Achou a placa, logo não tem porque iterar os demais contornos
                        break

                    else:
                        #Se área for menor placa_localizada é False
                        placa_localizada = False
                else:
                    #Se relação não bater placa_localizada é False
                    placa_localizada = False
            else:
                #Se o contorno não for um quadrilátero placa_localizada é False
                placa_localizada = False

        #Se a placa foi localizada
        if placa_localizada:

            #Se a placa ainda não foi lida
            if placa == None:

                #Aplicando uma máscara para criar uma imagem com somente a placa e o resto escuro
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [location], 0, 255, -1)
                new_image = cv2.bitwise_and(roi, roi, mask=mask)

                #Criando uma imagem nova só com a placa
                (x, y) = np.where(mask==255)
                (x1, y1) = (np.min(x), np.min(y))
                (x2, y2) = (np.max(x), np.max(y))
                cropped_image = gray[x1:x2+5, y1:y2+5]

                #Usando easyocr para ler a placa usando a imagem recortada
                result = reader.readtext(cropped_image)

                #Filtrando o resultado do easyocr para pegar somente o número da placa e não a localização
                numPlaca = filtar_placa(cropped_image, result, 0.6)

                #Se o número da placa foi lido com sucesso
                if numPlaca != None:

                    #Tirando espaços dentro do número da placa
                    numPlaca = numPlaca.replace(" ", "")

                    #Checando se a quantidade de caracteres dentro da placa bate com uma placa real
                    if len(numPlaca) == 7:

                        #Printando a placa
                        print(numPlaca)

                        #Iniciando variável de controle
                        placa_invalida = False

                        #Iterando cada caractere do número da placa lido
                        for i in range(0, len(numPlaca)):
                            
                            #Checando se os 3 primeiros digitos são letras, se não for, placa_invalida se torna True
                            if i < 3:
                                if numPlaca[i] not in letters:
                                    placa_invalida = True
                                    break
                            
                            #Checando se o quarto dígito é número, se não for, placa_invalida se torna True
                            elif i == 3:
                                if numPlaca[i] not in nums:
                                    placa_invalida = True
                                    break
                            
                            #Checando se o quinto dígito é um número ou letra, se não for, placa_invalida se torna True
                            elif i == 4:
                                if numPlaca[i] not in nums or numPlaca[i] not in letters:
                                    placa_invalida = True
                                    break
                            
                            #Checando se os dois últimos dígitos são números, se não for, placa_invalida se torna True
                            elif i > 4:
                                if numPlaca[i] not in nums:
                                    placa_invalida = True
                                    break

                        #Se a placa não for inválida
                        if not placa_invalida:

                            #É atribuido o valor da placa a variável placa
                            placa = numPlaca
                            
                            #Deleta o conteúdo da Entry da interface
                            interface.cplaca.delete(0, END) 

                            #Insere a placa na Entry da interface
                            interface.cplaca.insert(0, placa.upper())
                            
                            #Chama método inserir da interface
                            interface.inserir()

                    #Se o resultado que foi lído tem tamanho maior que o de uma placa maior     
                    else:
                        #O resultado é inválido e placa não é lida
                        placa = None

    #Se não foi detectada nenhuma placa na imagem
    else:
        #Se a quantidade de frames que se passaram desde que não é detectado 
        # uma placa na imagem for menor ou igual a 50
        if (framecount <= 50):

            #Adiciona um frame aos frames
            framecount += 1

            #Se a quantidade de frames for 50 e ja foi lido uma placa
            if framecount == 50 and placa != None:

                #Fecha a cancela
                interface.fecharCancela()
                
                #Nenhuma placa foi lida pois o carro passou da cancela
                placa = None
        
        #Se for maior que 50
        else:
            #Contagem de frames é zerada
            framecount = 0

    #Mostra o frame
    cv2.imshow("Imagem video", frame)

    return

#Essa é a função para filtrar o resultado do easyocr, usado na função acima
def filtar_placa(regiao, resultados, threshold):

    #Pega o tamanho da região (placa)
    tamanho = regiao.shape[0]*regiao.shape[1]

    #Inicializa o valor do número da placa
    numPlaca = None

    #Itera cada resultado que o easyocr leu
    for resultado in resultados:

        #Pega altura do que foi lido
        alt = np.sum(np.subtract(resultado[0][1], resultado[0][0]))
        
        #Pega largura do que foi lido
        larg = np.sum(np.subtract(resultado[0][2], resultado[0][1]))
        
        #Se o que foi lido for maior que 60% da placa é porque é o número da placa
        if alt*larg/tamanho > threshold:

            #Atribui o resultado ao número da placa
            numPlaca = resultado[1]

            #Retorna o número da placa
            return numPlaca        

#Essa função e as demais abaixo dessa são as funções de detecção de presença nas vagas
def camVaga6(frame, ard):
    #Inicializando variáveis a serem usadas        
    global ocupado6
    global framevaga6

    #Setando o ROI da vaga
    roi6 = frame[220: 450, 60: 280]
        
    #Transformando a imagem em escalas de cinza
    gray = cv2.cvtColor(roi6.copy(), cv2.COLOR_BGR2GRAY)
    
    #Borrando a imagem para reduzir ruídos
    blur = cv2.GaussianBlur(gray, (3,3), 1)

    #Binarizando a imagem
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    
    #Borrando a imagem para reduzir ruídos
    blur = cv2.medianBlur(Thresh, 5)

    #Aqui mostra a imagem binarizada (usado para debugging)
    #cv2.imshow("Blur", blur)
    
    #Pegando quantidade de pixeis brancos
    whitePixels = cv2.countNonZero(blur)
        
    #Se a quantidade de pixeis brancos forem maior que um valor e 
    # a variável de controle der como se a vaga não estivesse ocupada
    if (whitePixels > 5000 and not ocupado6):
        #Conta mais um frame da mudança de estado
        framevaga6 += 1

        #Se a quantidade de frames com o estado diferente for 10
        if framevaga6 == 10:

            #Reseta a variável de controle de mudança de estado
            framevaga6 = 0

            #Vaga é dada como ocupada
            ocupado6 = True
            print("Vaga6 ocupada")
            ard.desligaLED6()
        
    #Se a quantidade de pixeis for menor que um valor e 
    # a variável de controle der como se a vaga estivesse ocupada
    elif (whitePixels < 5000 and ocupado6):
        #Conta mais um frame da mudança de estado
        framevaga6 += 1

        #Se a quantidade de frames com o estado diferente for 10
        if framevaga6 == 10:

            #Vaga é dada como livre
            ocupado6 = False
            print("Vaga6 livre")
            ard.ligaLED6()
    
    #Caso a quantidade de pixeis forem maior que um valor mas a vaga ja estiver como ocupada 
    # ou a quantidade de pixeis forem menor que um valor mas a vaga ja estiver como livre
    # é resetado a quantidade de frames com a mudança de estado
    else:
        framevaga6 = 0

    #Mostrando o ROI
    #cv2.imshow("roi6", roi6)

    return

##### ************************OS MÉTODOS ABAIXO SÃO IGUAIS O MÉTODO ACIMA, LOGO NÃO IREI COMENTAR O MESMO ALGORITMO************************

def camVaga5(frame, ard):
    global ocupado5
    global framevaga5

    #Setando 
    roi5 = frame[210: 470, 260: 480]

    gray = cv2.cvtColor(roi5.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur", blur)
        
    whitePixels = cv2.countNonZero(blur)
        
    if (whitePixels > 5000 and not ocupado5):
        framevaga5 += 1
        if framevaga5 == 10:
            framevaga5 = 0
            ocupado5 = True
            print("Vaga5 ocupada")
            ard.desligaLED5()
        

    elif (whitePixels < 5000 and ocupado5):
        framevaga5 += 1
        if framevaga5 == 10:
            ocupado5 = False
            print("Vaga5 livre")
            ard.ligaLED5()
    
    else:
        framevaga5 = 0

    cv2.imshow("roi5", roi5)
    return

def camVaga4(frame, ard):
    global ocupado4
    global framevaga4

    roi4 = frame[230: 460, 460: 680]

    gray = cv2.cvtColor(roi4.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur", blur)
        
    whitePixels = cv2.countNonZero(blur)
        
    if (whitePixels > 5000 and not ocupado4):
        framevaga4 += 1
        if framevaga4 == 10:
            framevaga4 = 0
            ocupado4 = True
            print("Vaga4 ocupada")
            ard.desligaLED4()
        

    elif (whitePixels < 5000 and ocupado4):
        framevaga4 += 1
        if framevaga4 == 10:
            ocupado4 = False
            print("Vaga4 livre")
            ard.ligaLED4()
    
    else:
        framevaga4 = 0

    #cv2.imshow("roi4", roi4)
    return

def camVaga3(frame, ard):
    global ocupado3
    global framevaga3

    roi3 = frame[145: 420, 50: 230]

    gray = cv2.cvtColor(roi3.copy(), cv2.COLOR_BGR2GRAY)
    blur3 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur3 = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur3", blur3)
        
    whitePixels = cv2.countNonZero(blur3)
        
    if (whitePixels > 5000 and not ocupado3):
        framevaga3 += 1
        if framevaga3 == 10:
            framevaga3 = 0
            ocupado3 = True
            print("Vaga3 ocupada")
            ard.desligaLED3()
        

    elif (whitePixels < 5000 and ocupado3):
        framevaga3 += 1
        if framevaga3 == 10:
            ocupado3 = False
            print("Vaga3 livre")
            ard.ligaLED3()
    
    else:
        framevaga3 = 0

    cv2.imshow("Roi3", roi3)
    return

def camVaga2(frame, ard):
    global ocupado2
    global framevaga2

    roi2 = frame[145: 420, 260: 420]

    gray = cv2.cvtColor(roi2.copy(), cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur2 = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur2", blur2)
        
    whitePixels = cv2.countNonZero(blur2)
        
    if (whitePixels > 5000 and not ocupado2):
        framevaga2 += 1
        if framevaga2 == 10:
            framevaga2 = 0
            ocupado2 = True
            print("Vaga2 ocupada")
            ard.desligaLED2()
        

    elif (whitePixels < 5000 and ocupado2):
        framevaga2 += 1
        if framevaga2 == 10:
            ocupado2 = False
            print("Vaga2 livre")
            ard.ligaLED2()
    
    else:
        framevaga2 = 0

    #cv2.imshow("Roi2", roi2)
    return

def camVaga1(frame, ard):
    global ocupado1
    global framevaga1

    roi1 = frame[210: 450, 420: 660]

    gray = cv2.cvtColor(roi1.copy(), cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur1 = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur1", blur1)
        
    whitePixels = cv2.countNonZero(blur1)
        
    if (whitePixels > 5000 and not ocupado1):
        framevaga1 += 1
        if framevaga1 == 10:
            framevaga1 = 0
            ocupado1 = True
            print("Vaga1 ocupada")
            ard.desligaLED1()
        

    elif (whitePixels < 5000 and ocupado1):
        framevaga1 += 1
        if framevaga1 == 10:
            ocupado1 = False
            print("Vaga1 livre")
            ard.ligaLED1()
    
    else:
        framevaga1 = 0

    #cv2.imshow("Roi1", roi1)
    return

