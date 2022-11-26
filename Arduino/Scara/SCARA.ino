//LIBRARIES:
#include <Servo.h> 
#include <AFMotor.h>

AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

Servo myservo1;  //creamos un objeto servo 
Servo myservo2;  //creamos un objeto servo 

bool finCadena = false;
String Aux = "";
String Orientacion = "";
String cadenaCharEntrada = "";
String cadenaNumeroGrado = "";

int pos=90;
int i=0;

char *Cadenas ;

int angulo;
int aux;
int Total,Part1;
int Grado;
int Pos_futura=0;
int Pos_actual=0;
int Pasos=0;

void setup(){
  //Serial.println("Stepper test!");
  motor1.setSpeed(50); // 50 rpm
  motor2.setSpeed(20); // 50 rpm
  myservo1.attach(10);  // asignamos el pin 11 al servo1 codo 1
  myservo2.attach(9);  //   asignamos el pin 9 al servo2 codo 2
  
  Serial.begin(9600); // iniciamos el puerto serial
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

void Servo1(int angulo){

  myservo1.write(angulo);
  //Serial.print("ángulo 1:  ");
  //Serial.println(angulo);
  delay(2000);  

}
void Servo2(int pinza){

  if (pinza == 0){angulo = 180;}
  else if (pinza == 1){angulo = 70;}

  myservo2.write(angulo);
  // Serial.print("ángulo 3:  ");
  // Serial.println(angulo);
  delay(2000);

}
void Base(int angulo){
  if ((angulo == 0) && (Pasos != 0)){
      Pasos = Pos_actual*4000/17;
      motor1.step(Pasos, BACKWARD, SINGLE);
      Pos_futura=0;
      Pos_actual=0;
      
      //Serial.println(Pasos);
      //Serial.println("memoria");
    }
  else {
    Pos_futura = angulo ;
    Pasos = abs(( Pos_futura - Pos_actual ))*4000/17;
    if (Pos_futura < Pos_actual){motor1.step(Pasos, BACKWARD, SINGLE);}
    else{motor1.step(Pasos, FORWARD, SINGLE);}
    
    Pos_actual = angulo;
   //Serial.println(Pasos);
   //Serial.println("angulo");
  }
}
void Braso(int angulo){
  if ((angulo == 0) && (Pasos != 0)){
      Pasos = Pos_actual*200/360;
      motor2.step(Pasos, FORWARD, SINGLE);
      Pos_futura=0;
      Pos_actual=0;
      
      //Serial.println(Pasos);
      //Serial.println("memoria");
    }
  else {
    Pos_futura = angulo ;
    Pasos = abs(( Pos_futura - Pos_actual ))*200/360;
    if (Pos_futura < Pos_actual){motor2.step(Pasos, FORWARD, SINGLE);}
    else{motor2.step(Pasos, BACKWARD, SINGLE);}
    
    Pos_actual = angulo;
   Serial.println(Pasos);
   Serial.println("angulo");
  }
}

//----------Seleccion
void Select(String Aux , int Grado){

  if (Aux=="Eb"){aux=1;}//Serial.println(aux);} // BASE
  else if (Aux=="Ebr"){aux=2;}//Serial.println(aux);} //BRASO
  else if (Aux=="Eab"){aux=3;}//Serial.println(aux);}  //ANTEBRASO
  else if (Aux=="E"){aux=4;}//Serial.println(aux);} //PINZA


  switch (aux) {
    //----------------------SERVO 1 CODO 1 360 - on vel 
    case 1:
      //Serial.println(Grado);
      aux = 0;
      Base(Grado);
      break;
    //----------------------SERVO 2 CODO 2
      case 2:
        aux = 0;
        Braso(Grado);
      break;
    //----------------------SERVO 3 PINZA
      case 3:
        aux = 0;
        Servo1(Grado);

      break;
    //----------------------Paso a paso - base
      case 4:
        aux = 0;
        Servo2(Grado);
        

      break;

      default:
      break;
  }
}
