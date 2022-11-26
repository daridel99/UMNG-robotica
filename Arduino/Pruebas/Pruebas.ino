String cadenaCharEntrada = "";
String Aux = "";
char *Ident;
int Total;
bool finCadena = false;

void setup() {
  
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);   

}

void loop() {
  if (finCadena==true) //Si la bandera finCadena = 1, entonces la transmision esta completa
  {
    Aux = cadenaCharEntrada;   
    Ident = strtok(Aux.c_str(), ",");
    Serial.println(Ident); 
    Select(Ident);        
    finCadena=false;
    cadenaCharEntrada = "";
  }  
}


void serialEvent(){
  //Recepción de datos Seriales
  while (Serial.available()) {              //Si existen datos seriales, leer a todos
    char CaracterEntrada = Serial.read();   //Leer 1 byte serial recibido   
    cadenaCharEntrada += CaracterEntrada;  
    //Agregar el nuevo char a una cadena String 
    if (CaracterEntrada == '\n') {             //Si el char o byte recibido es un fin de linea, activa la bandera
      finCadena = true;                        
    }   
  }
}

void Select(String Aux){

  if (Aux =="A" || Aux=="Ab" || Aux=="Abr" || Aux=="Aab")
  {
   Serial2.println(cadenaCharEntrada);    
  }
  else if (Aux =="E" || Aux=="Eb" || Aux=="Ebr" || Aux=="Eab")
  {
   Serial1.println(cadenaCharEntrada);
  } 
}
