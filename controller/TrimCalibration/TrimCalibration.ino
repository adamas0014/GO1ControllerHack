#include <Arduino.h>
#include <String>

#define X_JOY A0 
#define Y_JOY A1
#define X_OUT DAC0
#define Y_OUT DAC1


int xJoy, yJoy, xMapped, yMapped;
int adcRangeInput[2] = {0, 1024};
int dacRangeOutput[2] = {0, 4096};


void setup() {

  pinMode(X_OUT, OUTPUT);
  pinMode(Y_OUT, OUTPUT);

  pinMode(X_JOY, INPUT);
  pinMode(Y_JOY, INPUT);

  Serial.begin(9600);
  analogWriteResolution(12);
}

void loop() {

  while (true){
    xJoy = analogRead(X_JOY);
    yJoy = analogRead(Y_JOY);
    
    xMapped = map(xJoy, adcRangeInput[0], adcRangeInput[1], dacRangeOutput[0], dacRangeOutput[1]) - 1052;
    yMapped = map(yJoy, adcRangeInput[0], adcRangeInput[1], dacRangeOutput[0], dacRangeOutput[1]) - 1052;
    
    //Clamp
    if(xMapped < dacRangeOutput[0]) xMapped = dacRangeOutput[0];
    else if(xMapped > dacRangeOutput[1]) xMapped = dacRangeOutput[1];

    if(yMapped < dacRangeOutput[0]) yMapped = dacRangeOutput[0];
    else if(yMapped > dacRangeOutput[1]) yMapped = dacRangeOutput[1];

    Serial.println("[ " + String(xMapped) + ", " + String(yMapped) + " ]");

    analogWrite(X_OUT, xMapped);
    analogWrite(Y_OUT, yMapped);
    
    delay(50);
  
  }

  
}
