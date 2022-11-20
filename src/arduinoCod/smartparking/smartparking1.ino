#include <Servo.h>

#define pinServo1 6
#define pinServo2 7
#define LED1 2
#define LED2 3
#define LED3 4
#define LED4 5
#define LED5 8
#define LED6 9

int botao = 10;
int pressionado = 0;
Servo servo1;
Servo servo2;

void setup() {
  	// put your setup code here, to run once:
  	Serial.begin(9600);
  	servo1.attach(pinServo1);
  	servo2.attach(pinServo2);
	pinMode(LED1, OUTPUT);
  	pinMode(LED2, OUTPUT);
  	pinMode(LED3, OUTPUT);
  	pinMode(LED4, OUTPUT);
  	pinMode(LED5, OUTPUT);
  	pinMode(LED6, OUTPUT);
  	pinMode(botao, INPUT);
  	Serial.print("\nComecou");
}

void loop() {
  	// put your main code here, to run repeatedly:

  	if(Serial.available() > 0){
    	String msg = Serial.readString();
      	Serial.print("\n" + msg);
      	read_protocol(msg);
  	}
  
  	pressionado = digitalRead(botao);
    
	if (pressionado == HIGH){
		//Serial.print("CAM");
	} 
}

void desligaLED(String msg){
	char pin = msg[3];
  	Serial.print("\n" + pin);
    
    if(pin == '1'){
		digitalWrite(LED1, LOW);
    }
  	if(pin == '2'){
		digitalWrite(LED2, LOW);
    }
  	if(pin == '3'){
		digitalWrite(LED3, LOW);
    }
  	if(pin == '4'){
		digitalWrite(LED4, LOW);
    }
  	if(pin == '5'){
		digitalWrite(LED5, LOW);
    }
  	if(pin == '6'){
		digitalWrite(LED6, LOW);
    }   
}

void ligaLED(String msg){
	char pin = msg[3];
  	Serial.print("a");
  
    if(pin == '1'){
      	Serial.print("b");
		digitalWrite(LED1, HIGH);
    }
  	if(pin == '2'){
		digitalWrite(LED2, HIGH);
    }
  	if(pin == '3'){
		digitalWrite(LED3, HIGH);
    }
  	if(pin == '4'){
		digitalWrite(LED4, HIGH);
    }
  	if(pin == '5'){
		digitalWrite(LED5, HIGH);
    }
  	if(pin == '6'){
		digitalWrite(LED6, HIGH);
    }   
}

void commandLED(String msg){
	String command = "";
  
  	for (int i = 4; i < 6; i++){
		command = command + msg[i];
    }
  	Serial.print("\n" + command);
         
    if(command == "ON"){
		ligaLED(msg);
    }
         
    if(command == "OF"){
		desligaLED(msg);
    }
}
         
void read_protocol(String msg){
	String component = "";
  
  	for (int i = 0; i < 3; i++){
		component = component + msg[i];
    }
  	Serial.print("\n" + component);
         
    if (component == "LED"){
		commandLED(msg);
    }
    if (component == "SRV"){
		commandCancela(msg);
    }
  	
}

void commandCancela(String msg){
	String command = "";
  
  	for (int i = 4; i < 6; i++){
		command = command + msg[i];
    }
  	Serial.print("\n" + command);
         
    if(command == "OP"){
		  abrirCancela(msg);
    }
         
    if(command == "CL"){
		  fecharCancela(msg);
    }
}

void fecharCancela(String msg){
  char pin = msg[3];
  
  if (pin == '1'){
    for (int i = 0; i <= 90; i++){
      	servo1.write(i);
      	delay(30);
    }    
  }
  
  if (pin == '2'){
    for (int i = 0; i <= 90; i++){
      	servo2.write(i);
      	delay(30);
    }    
  }
}
void abrirCancela(String msg){
	char pin = msg[3];
    
    if (pin == '1'){
    	for (int i = 90; i >= 0; i--){
      		servo1.write(i);
      		delay(30);
    	}
    }
  
  	if (pin == '2'){
    	for (int i = 90; i >= 0; i--){
      		servo2.write(i);
      		delay(30);
    	}
    }
}