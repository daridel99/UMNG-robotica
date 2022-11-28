bool finCadena = false;
String Aux = "";
String cadenaCharEntrada = "";
int Grado;
int Pos_actual=0;
int Pos_futura=0;
int Pasos=0;
float resolucion=0;
int maximos =4000;
int refe=17;

void setup() {
  Serial.begin(9600);
  resolucion=(float) maximos/refe;
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  if (finCadena) {    
    Aux = cadenaCharEntrada;   
    Grado = atoi(Aux.c_str());
    Base(Grado);    
    cadenaCharEntrada = "";
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

void Base(int angulo){  
      Pos_futura = angulo ;     
      Pasos = abs(Pos_futura - Pos_actual) * resolucion;
      Serial.println(Pasos);   
      Pos_actual = angulo;
      Serial.println(Pos_actual);
}
