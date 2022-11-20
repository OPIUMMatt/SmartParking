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
serialInst.open()
