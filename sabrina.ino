//Libraries
#include <Event.h>
#include <Timer.h>
#include <LiquidCrystal.h>
#include <DHT.h>
//Constants
#define DHTPIN 11    // what pin we're connected to
#define SWITCH1 A5    // what pin we're connected to
#define SWITCH2 12    // what pin we're connected to
#define SWITCH3 2    // what pin we're connected to
#define DHTTYPE DHT11   // DHT 22  (AM2302)
#define ALARM 10


#define ON   0
#define OFF  1
#define PERIOD 60UL*60UL*12UL*1000UL
//Crear el objeto LCD con los números correspondientes (rs, en, d4, d5, d6, d7)
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

//Variables
int lightState;
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value
bool tempCritical = false;

Timer t;

void setup(){  
  lcd.begin(16, 2);
  pinMode(SWITCH1,OUTPUT);
  pinMode(SWITCH2,OUTPUT);
  pinMode(SWITCH3,OUTPUT);
  pinMode(ALARM, OUTPUT); // Set buzzer
  Serial.begin(9600);
  dht.begin(); 
  int tickEvent1 = t.oscillate(SWITCH1, PERIOD , ON); //5 seg
  int tickEvent2 = t.oscillate(SWITCH3, PERIOD , ON);
  t.every(1000,sense);
  Serial.print("2 second tick started id=");
  Serial.println(tickEvent1);
  Serial.print("2 second tick started id=");
  Serial.println(tickEvent2);
}

void loop(){
  if(tempCritical){
    digitalWrite(SWITCH1,OFF);
    digitalWrite(SWITCH2,OFF);
    digitalWrite(SWITCH3,OFF);
    tone(ALARM, 1000); // Send 1KHz sound signal...
    lcd.home();
    lcd.clear();
    lcd.print("TEMPERATURA SUPERADA");
    delay(6000);
  }else{
    t.update();
  }
}

void sense(){
  //Read data and store it to variables hum and temp
  hum = dht.readHumidity();
  temp= dht.readTemperature();
  //Print temp and humidity values to serial monitor
  //Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.print("\t");
  //Serial.print(" %, Temp: ");
  Serial.println(temp);
  //Serial.println(" Celsius");

  if(temp >= 40){
    tempCritical = true;
  }else if(temp >= 30){
    digitalWrite(SWITCH2,ON);
  }else{
    digitalWrite(SWITCH2,OFF);
  }
  lcd.home();
  lcd.clear();
  //lcd.setCursor(0, 0);
  lcd.print("Humedad: ");
  lcd.print(hum);
  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temp);
}
