//LIBRARIES:
#include <Servo.h> 
#include <AFMotor.h>

AF_Stepper motor1(200, 1);
AF_Stepper motor2(200, 2);

Servo myservo1;  //creamos un objeto servo 
Servo myservo2;  //creamos un objeto servo 

bool finCadena = false;

String Aux = "";
String cadenaCharEntrada = "";
String cadenaNumeroGrado = "";

char *Cadenas ;

int angulo;
int aux;
int Total,Part1;
int Grado;
int Pos_Futura_Base=0;
int Pos_Actual_Base=0;
int Pasos=0;
int Pos_Futura_Brazo=0;
int Pos_Actual_Brazo=0;
int Maximos_Base =4000;
int Refe_Base=17;
int Maximos_Brazo =10;
int Refe_Brazo=9;

float Resolucion_Base=0;
float Resolucion_Brazo=0;


void setup(){
  motor1.setSpeed(50); // 50 rpm
  motor2.setSpeed(10); // 50 rpm
  myservo1.attach(10); //Pin 11 al servo1 (codo 1)
  myservo2.attach(9);  //Pin 9 al servo2 (codo 2)  
  Serial.begin(9600); // iniciamos el puerto serial
  Resolucion_Base=(float) (Maximos_Base/Refe_Base); 
  Resolucion_Brazo=(float) (Maximos_Brazo/Refe_Brazo); 
  motor2.step(5, FORWARD, INTERLEAVE);
  delay(20);
  myservo1.write(95);
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
    Select(Cadenas,Grado);    
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
  angulo = map(angulo, -90, 90, 20, 170);
  myservo1.write(angulo);
}

void Servo2(int pinza){
  if (pinza == 0){angulo = 180;}
  else if (pinza == 1){angulo = 70;}
  myservo2.write(angulo);
}

void Base(int angulo){
  if ((angulo == 0) && (Pasos != 0)){
      Pasos = Pos_Actual_Base * Resolucion_Base;
      motor1.step(Pasos, BACKWARD, SINGLE);
      Pos_Futura_Base=0;
      Pos_Actual_Base=0;
    }
  else {
    Pos_Futura_Base = angulo ;
    Pasos = abs(Pos_Futura_Base - Pos_Actual_Base) * Resolucion_Base;
    if (Pos_Futura_Base < Pos_Actual_Base){motor1.step(Pasos, BACKWARD, SINGLE);}
    else{motor1.step(Pasos, FORWARD, SINGLE);}  
    Pos_Actual_Base = angulo;    
  }
}

void Braso(int angulo){
  angulo = map(angulo, -90, 90, -100, 100);
  if ((angulo == 0) && (Pasos != 0)){
      if (Pos_Actual_Brazo<0)
      {
        Pasos = -Pos_Actual_Brazo * Resolucion_Brazo;      
        motor2.step(Pasos, BACKWARD, INTERLEAVE);      
      }
      else
      {
        Pasos = Pos_Actual_Brazo * Resolucion_Brazo;      
        motor2.step(Pasos,FORWARD, INTERLEAVE);      
      }
      Pos_Futura_Brazo=0;
      Pos_Actual_Brazo=0;
    }
  else {
    Pos_Futura_Brazo = angulo ;
    Pasos = abs(Pos_Futura_Brazo - Pos_Actual_Brazo) * Resolucion_Brazo;
    if (Pos_Futura_Brazo < Pos_Actual_Brazo){motor2.step(Pasos, FORWARD, INTERLEAVE);}
    else{motor2.step(Pasos, BACKWARD, INTERLEAVE);}
    Pos_Actual_Brazo = angulo;    
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
