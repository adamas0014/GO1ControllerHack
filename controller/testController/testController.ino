#include <Arduino.h>
#include <String>


void setup() {

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);

  Serial.begin(9600);




}

void loop() {
  

  

  while (Serial.available() > 0){

    bool ret = false;
    String data;
 
    while (!ret){
      char character = Serial.read();
      //Serial.println(character);
      if(character == '\n'){
        ret = true;
      }
      else{
        data += character;
      }

    }


    if(data[0] == 'F'){
      digitalWrite(8, HIGH);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
    }
    else if (data[0] == 'B'){
      Serial.println("B9");
      digitalWrite(8, LOW);
      digitalWrite(9, HIGH);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
    }
    else if (data[0] == 'L'){
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, HIGH);
      digitalWrite(11, LOW);
    }
    else if (data[0] == 'R'){
      
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, HIGH);
    }
    else{
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      Serial.println("Nothing");
    }

    

  }

  




}