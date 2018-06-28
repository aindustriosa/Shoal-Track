// -*- mode: C++ -*-
/*
 * ShoalNode for ShoalTrack system
 * 
 * Description:
 * Sistema de adquisicion de datos por telemetria descentralizada. 
 * Sobre dispositivo ArduinoMini Pro (5v16Mhz) y Hardware de comunicacion RF430 SX1278 LoRa
 * Utiliza las librerias RadioHead para comunicacion con LoRa a traves de un protocolo mallado
 * Utiliza un protocolo propio (CardumeProtocol) para el envío de información.
 * GPS de la marca ublox (solo atraves del codigo binario)
 * IMU MPU6050
 * presion: BMP280
 * temperatura: 3x ds18b20
 * Luz: LDR
 * Voltage: ADC interno
 * Amperios: ADC interno
 * RGB: 4 x WS2812
 */

// 
#include <Arduino.h>



//TIME slots shedeluer
uint32_t timeNow=0; // Hold the milliseond value for now
uint32_t timerStore=0;   //El anterior valor del timer 
uint8_t cycleTimerCount=0;

uint8_t counter_1s = 8;




////////////////////////////////////////////////////////////////////////////////
//MAIN SETUP
////////////////////////////////////////////////////////////////////////////////
void setup() {
    delay(500); //para estabilzar voltajes
    
    timerStore=millis();
    timeNow=millis();
    delay(20);
  
}
 
////////////////////////////////////////////////////////////////////////////////
//MAIN LOOP
////////////////////////////////////////////////////////////////////////////////
void loop() {
    timeNow = millis();
    if (timeNow<timerStore){//se produce desvordamiento de buffer del timer32; reseteo la refernecia base
        timerStore=0;
    }
  
    if((timeNow-timerStore)>=20){  // Main loop runs at 50Hz -> 20 milisec
    
       cycleTimerCount++;
       
       // Do these things every 6th time through the main cycle 
       // This section gets called every 1000/(20*6) = 8 1/3 Hz
       // doing it this way removes the need for another 'millis()' call
       // and balances the processing load across main loop cycles.
       switch (cycleTimerCount) {
          case(0):
              //bloque potencia
             break;
 
          case(1): //se ejecuta cada segundo
             if (counter_1s == 0){
                
                counter_1s = 8;
            }else{
                counter_1s--;    
            }
             break;
                        
          case(2):
             //bloque GPS
             break;
                        
          case(3):
             //bloque de luzes
             break;
                
          case(4):
             //bloque de temperaturas y presion
             break;
                        
          case(5):
            //bloque trasmision
             cycleTimerCount = -1; // Reset case counter, will be incremented to zero before switch statement
            break;
        }
   }
}



