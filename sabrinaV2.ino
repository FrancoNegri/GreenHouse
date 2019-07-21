//Libraries
#include <Event.h>
#include <Timer.h>
#include <DHT.h>
#include <Servo.h> 
//Constants
#define DHTPIN 11    // what pin we're connected to
#define DHTTYPE DHT11   // DHT 22  (AM2302)
//Switches
#define SWITCH1 4    // what pin we're connected to
#define SWITCH2 5    // what pin we're connected to
#define SWITCH3 6    // what pin we're connected to
#define SWITCH4 7    // what pin we're connected to
//Other connectors
#define ALARM 10
#define LIGHTSENSOR A0
//SWITCH Utils
#define ON   0
#define OFF  1

DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

Servo myservo;  // create servo object to control a servo 
                // twelve servo objects can be created on most board

Timer t;

//Variables
bool tempCritical = false;
bool tapado = false;


void setup(){  
  pinMode(SWITCH1,OUTPUT);
  pinMode(SWITCH2,OUTPUT);
  pinMode(SWITCH3,OUTPUT);
  pinMode(SWITCH4,OUTPUT);
  pinMode(ALARM, OUTPUT); // Set buzzer
  Serial.begin(9600);
  dht.begin(); 
  //t.every(1000UL * 60UL,sense);
  t.every(1000UL,sense); //Testing
  sense();
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
}

void loop(){
  if(tempCritical){
    //SHUTDOWN ALL
    digitalWrite(SWITCH1,OFF);
    digitalWrite(SWITCH3,OFF);
//    digitalWrite(SWITCH3,OFF);
    digitalWrite(SWITCH4,OFF);
    tone(ALARM, 1000); // Send 1KHz sound signal...
    delay(6000);
  }else{
    handleSerial();
  }
  t.update();
}

void handleSerial() {
 while (Serial.available() > 0) {
   char incomingCharacter = Serial.read();
   switch (incomingCharacter) {
      //Greenhouse lights
      case '+':
        digitalWrite(SWITCH4,ON);
        digitalWrite(SWITCH2,ON);
      break;
 
      case '-':
        digitalWrite(SWITCH4,OFF);
        digitalWrite(SWITCH2,OFF);
      break;
      //heat
      case 'L':
        digitalWrite(SWITCH1,ON);
      break;
      case 'l':
        digitalWrite(SWITCH1,OFF);
      break;

      //tapa (T=tapado, t=noTapado) 
      case 'T':
          myservo.write(90);
          tapado = true;
      break;
      case 't':
        myservo.write(0);
        tapado = false;
      break;
     }
  }
}

void sense(){
  float hum;  //Stores humidity value
  float temp; //Stores temperature value
  int light = analogRead(LIGHTSENSOR);
  //Read data and store it to variables hum and temp
  hum = dht.readHumidity();
  temp= dht.readTemperature();
  //Print temp and humidity values to serial monitor
  //humidity temp light tapado switch1 switch2 switch3 switch4
  Serial.print(hum);
  Serial.print("\t");
  Serial.print(temp);
  Serial.print("\t");
  Serial.print(light);
  Serial.print("\t");
  Serial.print(tapado);
  Serial.print("\t");
  Serial.print(!digitalRead(SWITCH1));
  Serial.print("\t");
  Serial.print(!digitalRead(SWITCH2));
  Serial.print("\t");
  Serial.print(!digitalRead(SWITCH3));
  Serial.print("\t");
  Serial.print(!digitalRead(SWITCH4));
  Serial.println();
  if(temp >= 40){
    tempCritical = true;
  }

  if(temp >= 30){
    digitalWrite(SWITCH3,ON);
  }else{
    digitalWrite(SWITCH3,OFF);
  }
}
