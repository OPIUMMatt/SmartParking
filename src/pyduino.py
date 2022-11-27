import serial.tools.list_ports

def abrirCancela1():
    command = "SRV1OP"
    serialInst.write(command.encode('utf-8'))

def fecharCancela1():
    command = "SRV1CL"
    serialInst.write(command.encode('utf-8'))

def abrirCancela2():
    command = "SRV2OP"
    serialInst.write(command.encode('utf-8'))

def fecharCancela2():
    command = "SRV2CL"
    serialInst.write(command.encode('utf-8'))

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

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = "COM3";

for x in range(0, len(portsList)):
    if portsList[x].startswith(val):
        portVar = val

serialInst.baudrate = 9600
serialInst.port = portVar

if not serialInst.isOpen():
    serialInst.open()
