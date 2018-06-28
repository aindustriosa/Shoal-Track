// -*- mode: C++ -*-
/*
 * ShoalGateway for ShoalTrack2018 system
 * 
 * Description:
 * Sistema de adquisicion de datos por telemetria descentralizada. 
 * Gateway to PC sobre dispositivo ArduinoMini Due y Hardware de comunicacion RF430 SX1278 LoRa
 * Utiliza las librerias RadioHead para comunicacion con LoRa a traves de un protocolo mallado
 * Utiliza un protocolo propio (CardumeProtocol) para el envío de información.
 * GPS de la marca ublox (solo atraves del codigo binario) UbxGps
 * Luz: 1xLDR
 * Sonda Vaisala WXT520
 */

#include "config.h"
#include <Arduino.h>
#include <RH_RF95.h> //para cargar el hardware de comunicaicones LoRa
#include <CardumeLink.h>
#include "Statistic.h"

//sistema gps:
#include <GPSUbloxBinary.h>

//para la sonda vaisala
#include <Vaisala_WXT520.h>


// Singleton instance of the radio driver (420 bytes de RAM y 5.4 Kb de FLASH)
RH_RF95 cardume_driver; 

//creamos el manager de comunicaicones: (827 bytes de RAM y 2.5 Kb de FLASH)
CardumeLink net_manager(cardume_driver, CARDUME_ADDRESS);// 

//creamos el enlaceGPS
//NAV-PVT (Navigation Position Velocity Time Solution)[p308]: iTOW, year, month, day, hour, min, sec, valid, 
//tAcc, nano, fixType, flags, reserved1, numSV, lon, lat, height, hMSL, hAcc, vAcc, velN, velE, velD, 
//gSpeed, heading, sAcc, headingAcc, pDOP, reserved2, reserved3.
GPSUbloxBinary gps(GPSPort);
uint32_t timeGPSref; // Hold the milliseond 


//Meteo sensor vaisala:
static Vaisala_WXT520 vaisala_sensor(VaisalaPort);

//TIME slots shedeluer
static uint8_t status; //parasaber si algo va mal...
uint32_t timeNow=0; // Hold the milliseond value for now
uint32_t timerStore=0;   //El anterior valor del timer 
int8_t cycleTimerCount=0;

uint8_t counter_1sA = 8;
uint8_t counter_1sB = 8;
uint8_t counter_3s = 24;


//variables de comunicaciones:
static crdm_Keys_t sh_keys ={ 0,"GWRS01",
                      {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       201, 202, 203, 204, 205, 206, 207, 208, 209, 210,211, 212, 213, 214, 215, 227},
                      {101,102,103,104,105,106,107,108},
                      {109, 110, 111, 112, 113, 114, 115, 116},
                      {0,0,0,0}
 };
Packet_Header_t  sh_header; //la parte dela cabezera y el tiempo


Packet_ShoalTrackReport_t sh_report; //los trama de sensorica
Packet_TraceRouteReport_t sh_traceroute; //los trama de traceroute
Packet_MeteoWindReport_t sh_meteowindreport; //los trama de metereologia viento
Packet_MeteoTHPReport_t sh_meteothpreport; //los trama de metereologia viento
Packet_MeteoRainReport_t sh_meteorainreport; //los trama de metereologia viento

////////////////////////////////////////////////////////////////////////////////
//MAIN SETUP
////////////////////////////////////////////////////////////////////////////////
void setup() {
    delay(500); //para estabilzar voltajes
    GatewayPort.begin(115200); //115200
    //GatewayPort.println("#DEBUG,[MAIN],ShoalTrack Gateway init...");
    delay(200);

    GPSPort.begin(9600);
    delay(50);
    GPSPort.flush();

     //activo la red
    delay(100);
    status = net_manager.initialize(&sh_keys);
    if (status < 1){
      GatewayPort.println("#DEBUG,[NETWORK],FAIL...");
    }
    
    timerStore=millis();
    timeNow=millis();
    cycleTimerCount = -1; // Reset case counter
    delay(20);
  
    //Confgure pinout
    pinMode(LDRPIN, INPUT);

    delay(200);
    sh_header.data.from=CARDUME_ADDRESS;
    sh_report.data.init();
    sh_traceroute.data.init();
    sh_meteowindreport.data.init();
    sh_meteothpreport.data.init();
    sh_meteorainreport.data.init();
    VaisalaPort.begin(19200);
    vaisala_sensor.initialize();
    delay(500);

    //GatewayPort.println("#DEBUG,[INIT],OK...");
  
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
       timerStore = timeNow; //pongo la nueva referencia
       cycleTimerCount++; //incremento el contador del shedeluer 
       
       // Do these things every 6th time through the main cycle 
       // This section gets called every 1000/(20*6) = 8 1/3 Hz
       // doing it this way removes the need for another 'millis()' call
       // and balances the processing load across main loop cycles.
       switch (cycleTimerCount) {
          case(0):
              //bloque potencia
              //get_data_power();
             break;
 
          case(1): //se ejecuta cada segundo
             if (counter_1sA == 0){
                get_vaisala_data();
                
                counter_1sA = 8;
             }else{
                counter_1sA--;    
             }
             break;
                        
          case(2):
             //bloque GPS
             get_data_gps();
             break;
                        
          case(3):
             if (counter_1sB == 0){
                //send_report();
                 send_traceroute();
                
                counter_1sB = 8;
             }else{
                counter_1sB--;    
             }
             
             break;
                
          case(4):
             //bloque IMU
              
             break;
                        
          case(5):
            //bloque trasmision
            handle_msg();
            cycleTimerCount = -1; // Reset case counter, will be incremented to zero before switch statement
            break;
        }
    }

}

void save_sh_header(void){
  //grabo el tiempo actual: lo saco del GPS
  //comparo el time sacado cuando cogi el gps, contra el time actual:
  // si supera los 1000 milisegundos, incremento el TIMEMARK de segundos.
    uint32_t second_offset;
    uint8_t min_offset;
    
    second_offset = (millis()-timeGPSref)/1000;
    
    if (second_offset>=1){
        min_offset = (uint8_t)second_offset/60; //el entero de los minuntos
        second_offset -= min_offset*60; //le resot los segundos correspondientes

        sh_header.data.min += min_offset; //meto el minuto de mas 
        sh_header.data.seg += (uint8_t)second_offset;
    }
}

void get_data_gps(void){
  //cojo el GPS 
  if (gps.ready())
    {
      timeGPSref = millis(); //cojo la referencia del tiempo interna del Nod
      //primero si esta la fecha ok
      if (gps.year<2018){
          sh_report.data.gps_precision=0;  //No time
          return; //esta todo mal
      } else {
          sh_report.data.gps_precision=1; //no fix
      }
      
      //cubro el blowue de memoria del tiempo:
      sh_header.data.year=gps.year-2000; //empieza en el 2000.
      sh_header.data.month=gps.month;
      sh_header.data.day=gps.day;
      sh_header.data.hour=gps.hour;
      sh_header.data.min=gps.min;
      sh_header.data.seg=gps.sec;

      //añado posiciones
      sh_traceroute.data.gps_longitude=gps.lon; 
      sh_traceroute.data.gps_latitude=gps.lat; 
      
      //ahora la precision de la medida
      if (gps.fixType<2){
          sh_traceroute.data.gps_precision=1;
      }else{
          
          if (gps.hAcc/1000<2){          //High
              sh_traceroute.data.gps_precision =7; 
          } else if (gps.hAcc/1000<10){  //HighLow
              sh_traceroute.data.gps_precision =6;
          }else if (gps.hAcc/1000<25){   //Medium
              sh_traceroute.data.gps_precision =5;
          }else if (gps.hAcc/1000<50){   //MediumLow
              sh_traceroute.data.gps_precision =4;
          }else if (gps.hAcc/1000<100){   //Low
              sh_traceroute.data.gps_precision =3;
          }else if (gps.hAcc/1000>100){   //LowLow
              sh_traceroute.data.gps_precision =2;
          }
      }
      
      sh_traceroute.data.gps_itow=gps.iTOW;
      //sh_traceroute.data.gps_heading =  (uint8_t)map((int)gps.headMot/ 100000.0, 0, 360, 0, 255);
      
    }
    
}

void handle_msg(void){
   status = net_manager.request_handle();
   if (status>9){ //la trama esta completa
       if (status == CARDUME_MSG_TOME){ //si es una trama para el gateway?
           //status = net_manager.get_header(&sh_header,1); // la decodifico
           if (status ==CARDUME_ID_SENDORDEN){
              //net_manager.get_payload(&sh_header)
           }
       }
       //aun asi, la envio siepre al PC para llevar un log..
       net_manager.relay_last_packet(GatewayPort); 
   }  
   //GatewayPort.print("\n#DEBUG,[NET],Incoming: ");
   //GatewayPort.println(status);
}

void send_traceroute(void){
   sh_traceroute.data.next_hop = net_manager.get_nexthop(CARDUME_GATEWAY_ADDRESS);
   sh_traceroute.data.rssi = net_manager.get_rssi();
   
  //send report:
    sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
    sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
    save_sh_header();//Actualizo el TimeMark

    //GatewayPort.println("\nREPORT: ");
    net_manager.relay_packet(CARDUME_ID_TRACEROUTE,
                             sh_header.msg,sh_traceroute.msg, GatewayPort);
  
}


void get_vaisala_data(void){
    
    status = vaisala_sensor.available();
    //GatewayPort.println(status,DEC);
    //VaisalaPort.println("0R2");
      if (status == VAISALA_PACKET_WINDRECIEVE){
          //GatewayPort.println("\nWIND: ");
          sh_meteowindreport.data.wind_direction_min   = vaisala_sensor.get_wind_direction_min();
          sh_meteowindreport.data.wind_direction_avg   = vaisala_sensor.get_wind_direction_avg();
          sh_meteowindreport.data.wind_direction_max   = vaisala_sensor.get_wind_direction_max();
          sh_meteowindreport.data.wind_speed_min       = vaisala_sensor.get_wind_speed_min();
          sh_meteowindreport.data.wind_speed_avg       = vaisala_sensor.get_wind_speed_avg();
          sh_meteowindreport.data.wind_speed_max       = vaisala_sensor.get_wind_speed_max();

          //send report:
          sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
          sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
          save_sh_header();//Actualizo el TimeMark
          net_manager.relay_packet(CARDUME_ID_METEOWIND,sh_header.msg,
                                   sh_meteowindreport.msg, GatewayPort);

      }else if (status == VAISALA_PACKET_TEMPRECIEVE){
          //GatewayPort.println("\nTEMP: ");
          sh_meteothpreport.data.air_temperature   = vaisala_sensor.get_air_temperature();
          sh_meteothpreport.data.relative_humidity = vaisala_sensor.get_relative_humidity();
          sh_meteothpreport.data.air_pressure      = vaisala_sensor.get_air_pressure();
      
          //send report:
          sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
          sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
          save_sh_header();//Actualizo el TimeMark
          net_manager.relay_packet(CARDUME_ID_METEOTHP, sh_header.msg,
                                   sh_meteothpreport.msg, GatewayPort);
      
      }else if (status == VAISALA_PACKET_RAINRECIEVE){
          //GatewayPort.println("\nRAIN: ");
          sh_meteorainreport.data.rain_accumulation   = vaisala_sensor.get_rain_accumulation();
          sh_meteorainreport.data.rain_duration       = vaisala_sensor.get_rain_duration();
          sh_meteorainreport.data.rain_intensity      = vaisala_sensor.get_rain_intensity();
          sh_meteorainreport.data.hail_accumulation   = vaisala_sensor.get_hail_accumulation();
          sh_meteorainreport.data.hail_duration       = vaisala_sensor.get_hail_duration();
          sh_meteorainreport.data.hail_intensity      = vaisala_sensor.get_hail_intensity();
          sh_meteorainreport.data.rain_peak_intensity = vaisala_sensor.get_rain_peak_intensity();
          sh_meteorainreport.data.hail_peak_intensity = vaisala_sensor.get_hail_peak_intensity();
      
          //send report:
          sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
          sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
          save_sh_header();//Actualizo el TimeMark
          net_manager.relay_packet(CARDUME_ID_METEORAIN, sh_header.msg,
                                   sh_meteorainreport.msg, GatewayPort);
      }
    
}
