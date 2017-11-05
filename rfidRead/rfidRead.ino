#include <SoftwareSerial.h>

SoftwareSerial RFID(6, 0);
String msg;
String ID ;  //string to store allowed cards

void setup()  
{
  Serial.begin(9600);
  Serial.println("Serial Ready");

  RFID.begin(9600);
  Serial.println("RFID Ready");
}

char c;

void loop(){
  
  while(RFID.available()>0){
    c=RFID.read(); 
    msg += c;
  }
  msg=msg.substring(1,13);
  if(msg != "")
    Serial.println(msg);
  msg="";
}



