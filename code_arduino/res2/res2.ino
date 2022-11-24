/*
  KARLA JUANITA BARON HURTADO
  FINAL DE ARDUINO MEGA
  ANTROPOMORFICO
*/
//LIBRARIES:
#include <Servo.h> 
#include <Stepper.h>

Stepper myStepper(200, 3, 4, 5, 6);


Servo myservo1;  //creamos un objeto servo 
Servo myservo2;  //creamos un objeto servo 
Servo myservo3;  //creamos un objeto servo 

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
  myservo1.attach(11);  // asignamos el pin 11 al servo1 codo 1
  myservo2.attach(9);  // asignamos el pin 9 al servo2 codo 2
  myservo3.attach(10); // asignamos el pin 11 al servo3 pinza

  myStepper.setSpeed(50); // base


  Serial.begin(9600); // iniciamos el puerto serial
  Serial1.begin(9600);
  Serial2.begin(9600);
}

 
void loop() { 

  if (finCadena) { // 
    //Serial.println(cadenaCharEntrada); //CADENA
    Total = strlen(cadenaCharEntrada.c_str());
    //Serial.println(Total); //TOTAL 7
    Aux = cadenaCharEntrada;
    Cadenas = strtok(Aux.c_str(), ",");  
    //Serial.println(Cadenas); //
    Part1 = strlen(Cadenas);
    //Serial.println(Part1); //PARTE INICIAL DE LA CADENA 3
    for (int i = Part1+1; i < Total ; i++){
      cadenaNumeroGrado += Aux[i];
    }
    //Serial.println(cadenaNumeroGrado);
    Grado = atoi(cadenaNumeroGrado.c_str());
    //Serial.println(Grado);
    Select(Cadenas,Grado);    

    cadenaCharEntrada = "";
    cadenaNumeroGrado = "";
    finCadena = false;
    
  } 
 

} 

void serialEvent(){
  //Recepción de datos Seriales
  while (Serial.available()) {              //Si existen datos seriales, leer a todos
    char CaracterEntrada = Serial.read();   //Leer 1 byte serial recibido
   
    cadenaCharEntrada += CaracterEntrada;   //Agregar el nuevo char a una cadena String 
    if (CaracterEntrada == '\n') {          //Si el char o byte recibido es un fin de linea, activa la bandera
      finCadena = true;                        //Si la bandera finCadena = 1, entonces la transmision esta completa
    }
    
  }
} 

//----------------FUNCIONES DE CADA SERVO


//----------Seleccion
void Select(String Aux , int Grado){

  if (Aux =="A" || Aux=="Ab" || Aux=="Abr" || Aux=="Aab"){
    Serial2.println(cadenaCharEntrada);
    Serial.println("ANTRO");
  
  } // Ab = base 1
  else if (Aux =="E" || Aux=="Eb" || Aux=="Ebr" || Aux=="Eab"){
    
    Serial1.println(cadenaCharEntrada);
    Serial.println("SCARA");
    } // Abr = brazo 2   

}
