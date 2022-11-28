#Esse arquivo guarda as funções que são usadas para efetuar a comunicação do app em python com o arduino

#Importando dependencias
import serial.tools.list_ports

#### FUNÇÕES

#Abrir cancela
def abrirCancela1():

    #Setando o comando para mandar (o protocolo é o seguinte: os 3 primeiros dígitos são referentes ao componente,
    # o quarto é referente a qual desses componentes 
    # e os 2 últimos é o comandoque irá executar)
    command = "SRV1OP"

    #Enviando o comando para abrir a cancela para o arduino
    serialInst.write(command.encode('utf-8'))

#Fechar cancela
def fecharCancela1():

    #Setando o comando para mandar
    command = "SRV1CL"

    #Enviando o comando para fechar a cancela para o arduino
    serialInst.write(command.encode('utf-8'))

##### ************************OS MÉTODOS ABAIXO SÃO IGUAIS O MÉTODO ACIMA, LOGO NÃO IREI COMENTAR O MESMO ALGORITMO************************

#### MÉTODOS DA CANCELA
def abrirCancela2():
    command = "SRV2OP"
    serialInst.write(command.encode('utf-8'))

def fecharCancela2():
    command = "SRV2CL"
    serialInst.write(command.encode('utf-8'))

#### MÉTODOS DOS LED'S
def ligaLED1():
    command = "LED1ON"
    serialInst.write(command.encode('utf-8'))

def ligaLED2():
    command = "LED2ON"
    serialInst.write(command.encode('utf-8'))

def ligaLED3():
    command = "LED3ON"
    serialInst.write(command.encode('utf-8'))

def ligaLED4():
    command = "LED4ON"
    serialInst.write(command.encode('utf-8'))

def ligaLED5():
    command = "LED5ON"
    serialInst.write(command.encode('utf-8'))

def ligaLED6():
    command = "LED6ON"
    serialInst.write(command.encode('utf-8'))

def desligaLED1():
    command = "LED1OF"
    serialInst.write(command.encode('utf-8'))

def desligaLED2():
    command = "LED2OF"
    serialInst.write(command.encode('utf-8'))

def desligaLED3():
    command = "LED3OF"
    serialInst.write(command.encode('utf-8'))

def desligaLED4():
    command = "LED4OF"
    serialInst.write(command.encode('utf-8'))

def desligaLED5():
    command = "LED5OF"
    serialInst.write(command.encode('utf-8'))

def desligaLED6():
    command = "LED6OF"
    serialInst.write(command.encode('utf-8'))


#Pegando todas as portas identificadas no computador
ports = serial.tools.list_ports.comports()

#Instanciando o serial
serialInst = serial.Serial()

#Inicializando a lista de portas
portsList = []

#Iterando cada porta
for onePort in ports:
    #Atribuindo a porta ä lista de portas
    portsList.append(str(onePort))

    #Printando as portas
    print(str(onePort))

#Setando qual porta usar
val = "COM3";

#Pegando a porta a ser usada
for x in range(0, len(portsList)):
    if portsList[x].startswith(val):
        portVar = val

#Setando configurações do serial
serialInst.baudrate = 9600
serialInst.port = portVar

#Iniciando comunicação com a porta
if not serialInst.isOpen():
    serialInst.open()
