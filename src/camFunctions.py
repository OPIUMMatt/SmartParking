from matplotlib import pyplot as plt
import  cv2
import numpy as np
import imutils
import time as t
import easyocr
from tkinter import END
#import pyduino as ard

ocupado1 = False
ocupado2 = False
ocupado3 = False
placa_detec = False
framecount = 0
placa = None

def camPlaca(frame, interface):
    global placa_detec
    global placa
    global framecount

    roi = frame[100: 400, 50: 650]

    ##Aplicando filtro cinza
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    #Aplicando filtro de edges
    bFilter = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(bFilter, 30, 200)

    cv2.imshow("gray", edged)

    keypoints = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 10, True)

        if len(approx) == 4:
            (x, y, lar, alt) = cv2.boundingRect(cnt)
            proporc = lar/alt
            if proporc > 1:
                area = lar*alt
                if area > 40000 and area < 60000:
                    cv2.rectangle(roi, (x, y), (x+lar, y+alt), (0, 255, 0), 2)
                    location = approx
                    placa_detec = True
                    framecount = 0
                    break

                else:
                    placa_detec = False
            else:
                placa_detec = False
        else:
            placa_detec = False

    if placa_detec:
        if placa == None:
            t.sleep(0.5)
            #Aplicando uma máscara para criar uma imagem com somente a placa e o resto escuro
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(roi, roi, mask=mask)

            #Criando uma imagem nova só com a placa
            (x, y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+5, y1:y2+5]
            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            placa_detec = False

            numPlaca = filtar_placa(cropped_image, result, 0.6)

            if numPlaca != None:
                numPlaca = numPlaca.replace(" ", "")
                if len(numPlaca) == 7:
                    placa_invalida = False
                    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

                    for i in range(0, len(numPlaca)):

                        if i < 3:
                            if numPlaca[i] in nums:
                                placa_invalida = True
                                break

                        elif i == 3:
                            if numPlaca[i] not in nums:
                                placa_invalida = True
                                break

                        elif i > 4:
                            if numPlaca[i] not in nums:
                                placa_invalida = True
                                break

                    
                    if not placa_invalida:
                        placa = numPlaca
                        
                        interface.cplaca.delete(0, END) 
                        interface.cplaca.insert(0, placa.upper())
                        interface.inserir()
                else:
                    placa = None

    else:
        if (framecount <= 50):
            framecount += 1
            if framecount == 50 and placa != None:
                interface.fecharCancela()
                placa = None
        else:
            framecount = 51

        

    placa_detec = False
    cv2.imshow("Roi", roi)

    return

def filtar_placa(regiao, resultados, threshold):
    tamanho = regiao.shape[0]*regiao.shape[1]

    numPlaca = None

    for resultado in resultados:
        alt = np.sum(np.subtract(resultado[0][1], resultado[0][0]))
        larg = np.sum(np.subtract(resultado[0][2], resultado[0][1]))

        if alt*larg/tamanho > threshold:
            numPlaca = resultado[1]
            return numPlaca        

def camVaga6(frame):        
    global ocupado6
    roi = frame[130: 300, 315: 475]

    gray = cv2.cvtColor(roi.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(Thresh, 5)

    cv2.imshow("Blur", blur)
        
    whitePixels = cv2.countNonZero(blur)
        
    if (whitePixels > 400 and not ocupado6):
        ocupado6 = True
        print("Vaga ocupada")
        #ard.desligaLED()

    elif (whitePixels < 400 and ocupado6):
        ocupado6 = False
        print("Vaga livre")
        #ard.ligaLED()

    cv2.imshow("Imagem video", roi)
    return

def camVaga5(frame):
    global ocupado5
    roi = frame[130: 300, 315: 475]

    gray = cv2.cvtColor(roi.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(Thresh, 5)

    cv2.imshow("Blur", blur)
        
    whitePixels = cv2.countNonZero(blur)
        
    if (whitePixels > 400 and not ocupado5):
        ocupado5 = True
        print("Vaga ocupada")
        #ard.desligaLED()

    elif (whitePixels < 400 and ocupado5):
        ocupado5 = False
        print("Vaga livre")
        #ard.ligaLED()

    cv2.imshow("Imagem video", roi)
    return

def camVaga4(frame):
    global ocupado4
    roi = frame[130: 300, 315: 475]

    gray = cv2.cvtColor(roi.copy(), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur = cv2.medianBlur(Thresh, 5)

    cv2.imshow("Blur", blur)
        
    whitePixels = cv2.countNonZero(blur)
        
    if (whitePixels > 400 and not ocupado4):
        ocupado4 = True
        print("Vaga ocupada")
        #ard.desligaLED()

    elif (whitePixels < 400 and ocupado4):
        ocupado4 = False
        print("Vaga livre")
        #ard.ligaLED()

    cv2.imshow("Imagem video", roi)
    return

def camVaga3(frame):
    global ocupado3
    roi3 = frame[145: 420, 50: 230]

    gray = cv2.cvtColor(roi3.copy(), cv2.COLOR_BGR2GRAY)
    blur3 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur3 = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur3", blur3)
        
    whitePixels = cv2.countNonZero(blur3)
        
    if (whitePixels > 5000 and not ocupado3):
        ocupado3 = True
        print("Vaga ocupada")
        #ard.desligaLED3()

    elif (whitePixels < 5000 and ocupado3):
        ocupado3 = False
        print("Vaga livre")
        #ard.ligaLED3()

    cv2.imshow("Roi3", roi3)
    return

def camVaga2(frame):
    global ocupado2
    roi2 = frame[145: 420, 260: 420]

    gray = cv2.cvtColor(roi2.copy(), cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur2 = cv2.medianBlur(Thresh, 5)

    #cv2.imshow("Blur2", blur2)
        
    whitePixels = cv2.countNonZero(blur2)
        
    if (whitePixels > 5000 and not ocupado2):
        ocupado2 = True
        print("Vaga ocupada")
        #ard.desligaLED2()

    elif (whitePixels < 5000 and ocupado2):
        ocupado2 = False
        print("Vaga livre")
            #ard.ligaLED2()

    cv2.imshow("Roi2", roi2)
    return

def camVaga1(frame):
    global ocupado1    
    roi1 = frame[145: 420, 380: 660]

    gray = cv2.cvtColor(roi1.copy(), cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray, (3,3), 1)
    Thresh = cv2.adaptiveThreshold(blur1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    blur1 = cv2.medianBlur(Thresh, 5)

    cv2.imshow("Blur1", blur1)
        
    whitePixels = cv2.countNonZero(blur1)
        
    if (whitePixels > 5000 and not ocupado1):
        ocupado1 = True
        print("Vaga ocupada")
        #ard.desligaLED1()

    elif (whitePixels < 5000 and ocupado1):
        ocupado1 = False
        print("Vaga livre")
        #ard.ligaLED1()

    cv2.imshow("Roi1", roi1)
    return

