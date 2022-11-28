//Importando dependencias
#include <Servo.h>

//Configurando os pinos do arduino
#define pinServo1 6
#define pinServo2 7
#define LED1 2
#define LED2 4
#define LED3 3
#define LED4 5
#define LED5 8
#define LED6 9

//Iniciando os servos
Servo servo1;
Servo servo2;

//Setup, roda uma única vez quando o arduino é iniciado
void setup() {
  	// Iniciando o serial
  	Serial.begin(9600);

	// Atribuindo os servos aos pinos
  	servo1.attach(pinServo1);
  	servo2.attach(pinServo2);

	// Atribuindo os LEDs e o modo dos pinos
	pinMode(LED1, OUTPUT);
  	pinMode(LED2, OUTPUT);
  	pinMode(LED3, OUTPUT);
  	pinMode(LED4, OUTPUT);
  	pinMode(LED5, OUTPUT);
  	pinMode(LED6, OUTPUT);

	// Printando começou no serial
  	Serial.print("\nComecou");
    
	// Ligando os LEDs
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED5, HIGH);
    digitalWrite(LED6, HIGH);
    
}

//Loop roda em looping
void loop() {

  	//Se tem algum serial a ser lido, le a mensagem e manda para a função de leitura do protocolo
  	if(Serial.available() > 0){
    	String msg = Serial.readString();
      	Serial.print("\n" + msg);
      	read_protocol(msg);
  	}
}

//Função para desligar os LEDs
void desligaLED(String msg){

	//Pega o quarto dígito para conferir qual LED é exatamente
	char pin = msg[3];

	//Printando no serial o pino lido (usado para debugging)
  	//Serial.print("\n" + pin);
    
	//Checando qual LED vai desligar
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

//Função para ligar os LEDs
void ligaLED(String msg){

	//Pega o quarto dígito para conferir qual LED é exatamente
	char pin = msg[3];
	
	//Printando no serial o pino lido (usado para debugging)
  	//Serial.print("\n" + pin);

	//Checando qual LED vai ligar
    if(pin == '1'){
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

//Função para filtrar qual comando de LED vai ser executado
void commandLED(String msg){

	//Pegando os últimos 2 dígitos que são referentes ao comando
	String command = "";
  	for (int i = 4; i < 6; i++){
		command = command + msg[i];
    }

	//Printando no serial o comando (usado para debugging)
  	//Serial.print("\n" + command);

	//Verificando qual comando de LED executar
    if(command == "ON"){
		ligaLED(msg);
    }
         
    if(command == "OF"){
		desligaLED(msg);
    }
}

//Função para ler o protocolo
void read_protocol(String msg){

	//Pegando os 3 primeiro dígitos referentes ao tipo de componente
	String component = "";
  	for (int i = 0; i < 3; i++){
		component = component + msg[i];
    }

	//Printando o tipo de componente lido (usado para debugging)
  	//Serial.print("\n" + component);

	//Verificando para qual tipo de componente o comando vai
    if (component == "LED"){
		commandLED(msg);
    }

    if (component == "SRV"){
		commandCancela(msg);
    }
  	
}

//Função para executar o comando da cancela
void commandCancela(String msg){

	//Pegando os últimos quatro digitos referentes ao comando da cancela
	String command = "";
  	for (int i = 4; i < 6; i++){
		command = command + msg[i];
    }

	//Printando o comando lido (usado para debugging)
  	//Serial.print("\n" + command);

	//Verificando qual comando de servo executar
    if(command == "OP"){
		  abrirCancela(msg);
    }
         
    if(command == "CL"){
		  fecharCancela(msg);
    }
}

void fecharCancela(String msg){

	//Pega o quarto dígito para conferir qual servo é exatamente
	char pin = msg[3];
	
	//Checando qual servo vai fechar
	if (pin == '1'){
		//Fechando a cancela 1, começa com ângulo de 90 e vai diminuindo até o angulo 0
    	for (int i = 90; i >= 0; i--){
      		servo1.write(i);
      		delay(30);
    	}    
  	}
  
  	if (pin == '2'){
		//Fechando a cancela 2, começa com ângulo de 0 e vai aumentando até o angulo 90
    	for (int i = 0; i <= 90; i++){
      		servo2.write(i);
      		delay(30);
    	}    
  	}
}

void abrirCancela(String msg){

	//Pega o quarto dígito para conferir qual servo é exatamente
	char pin = msg[3];
    
	//Checando qual servo vai abrir
    if (pin == '1'){
		//Abrindo a cancela 1, começa com ângulo de 0 e vai aumentando até o angulo 0
    	for (int i = 0; i <= 90; i++){
      		servo1.write(i);
      		delay(30);
    	}
    }
  
  	if (pin == '2'){
		//Abrindo a cancela 2, começa com ângulo de 90 e vai diminuindo até o angulo 0
    	for (int i = 90; i >= 0; i--){
      		servo2.write(i);
      		delay(30);
    	}
    }
}
