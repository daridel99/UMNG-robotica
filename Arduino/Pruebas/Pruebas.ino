#include <Servo.h> 

Servo myservo1;  //creamos un objeto servo 

bool finCadena = false;
String Aux = "";
String cadenaCharEntrada = "";
String cadenaNumeroGrado = "";

char *Cadenas ; 

int angulo;
int aux;
int Total,Part1;
int Grado;
int Pos_futura=0;
int Pos_actual=0;
int Pasos=0;

void setup(){
  myservo1.attach(8);    // Pin 11 al servo1 (Codo 1) 
  Serial.begin(9600); // iniciamos el puerto serial
}

 
void loop() { 
  if (finCadena) {
    Total = strlen(cadenaCharEntrada.c_str());
    Aux = cadenaCharEntrada;
    Cadenas = strtok(Aux.c_str(), ",");  
    Part1 = strlen(Cadenas);
    for (int i = Part1+1; i < Total ; i++){
      cadenaNumeroGrado += Aux[i];
    }
    Grado = atoi(cadenaNumeroGrado.c_str());
    Servo1(Grado);
    cadenaCharEntrada = "";
    cadenaNumeroGrado = "";
    finCadena = false;    
  } 
} 

void serialEvent(){                         //Recepción de datos Seriales  
  while (Serial.available()) {              //Si existen datos seriales, leer a todos
    char CaracterEntrada = Serial.read();   //Leer 1 byte serial recibido 
    cadenaCharEntrada += CaracterEntrada;   //Agregar el nuevo char a una cadena String 
    if (CaracterEntrada == '\n') {          //Si el char o byte recibido es un fin de linea, activa la bandera
      finCadena = true;                     //Si la bandera finCadena = 1, entonces la transmision esta completa
    }
  }
} 

//----------------FUNCIONES DE CADA SERVO

void Servo1(int angulo){  
  myservo1.write(angulo);
}
