#include <Stepper.h>
const int stepsPerRevolution = 200;  
Stepper myStepper(stepsPerRevolution, 3, 4, 5, 6);
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


void setup() {
myStepper.setSpeed(10);
Serial.begin(9600);
 myStepper.step(0);
}

void loop() {
  if (finCadena){
    Total = strlen(cadenaCharEntrada.c_str());
    Aux = cadenaCharEntrada;
    Cadenas = strtok(Aux.c_str(), ",");  
    Part1 = strlen(Cadenas);
    for (int i = Part1+1; i < Total ; i++){
      cadenaNumeroGrado += Aux[i];
    }
    Grado = atoi(cadenaNumeroGrado.c_str());
    Base(Grado);    
    cadenaCharEntrada = "";
    cadenaNumeroGrado = "";
    finCadena = false;
  }  
}

void serialEvent()                            //Recepción de datos Seriales 
{  
  while (Serial.available()) 
    {                                         //Si existen datos seriales, leer a todos
      char CaracterEntrada = Serial.read();   //Leer 1 byte serial recibido   
      cadenaCharEntrada += CaracterEntrada;   //Agregar el nuevo char a una cadena String 
      if (CaracterEntrada == '\n')            //Si el char o byte recibido es un fin de linea, activa la bandera
        {          
          finCadena = true;                   //Si la bandera finCadena = 1, entonces la transmision esta completa
        }    
     }
}
void Servo1(int angulo){  
  myservo1.write(angulo);
}
void Servo2(int angulo){
  angulo = map(angulo, 90, -90, 0, 180);
  myservo2.write(angulo); 
}
void Servo3(int pinza){
  if (pinza == 0){angulo = 90;}
  else if (pinza == 1){angulo = 0;}
  myservo3.write(angulo);
}
void Base(int angulo){  
  if ((angulo == 0) && (Pasos != 0)){
      Pasos = -Pos_actual*(5/9);
      Pos_futura=0;
      Pos_actual=0;
    }
  else {
    Pos_futura = angulo ;
    Pasos = ( Pos_futura - Pos_actual )*5/9;
    Pos_actual = angulo;
  }
  myStepper.step(Pasos);

}
//----------Seleccion
void Select(String Aux , int Grado){

  if (Aux=="Ab"){aux=4;}//Serial.println(aux);} // Ab = base 1
  else if (Aux=="Abr"){aux=1;}//Serial.println(aux);} // Abr = brazo 2 
  else if (Aux=="Aab"){aux=2;}//Serial.println(aux);} // Aab = antebrazo 3 
  else if (Aux=="A"){aux=3;}//Serial.println(aux);}

  switch (aux) {
    //----------------------SERVO 1 CODO 1 360 - on vel 
    case 1:
      aux = 0;
      Servo1(Grado);
      break;
    //----------------------SERVO 2 CODO 2
      case 2:
        aux = 0;
        Servo2(Grado);
      break;
    //----------------------SERVO 3 PINZA
      case 3:
        aux = 0;
        Servo3(Grado);
      break;
    //----------------------Paso a paso - base
      case 4:
        aux = 0;
        Base(Grado);
      break;
      default:
      break;
  }
}
