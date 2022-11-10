
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

    if(data[0] == 'S'){
      analogWrite(X_OUT, (int)(4095 * 0.5));
      analogWrite(Y_OUT, (int)(4095 * 0.5));
    }
    else if(data[0] == 'F'){
      analogWrite(X_OUT, (int)(4095 * 0.75));
      analogWrite(Y_OUT, (int)(4095 * 0.5));
    }
    else if (data[0] == 'B'){
      analogWrite(X_OUT, (int)(4095 * 0.25));
      analogWrite(Y_OUT, (int)(4095 * 0.5));
    }
    else if (data[0] == 'L'){
      analogWrite(X_OUT, (int)(4095 * 0.5));
      analogWrite(Y_OUT, (int)(4095 * 0.25));
    }
    else if (data[0] == 'R'){
      analogWrite(X_OUT, (int)(4095 * 0.5));
      analogWrite(Y_OUT, (int)(4095 * 0.25));
    }
    else{
      analogWrite(X_OUT, (int)(4095 * 0.5));
      analogWrite(Y_OUT, (int)(4095 * 0.5));
    }

    

  }

  




}
