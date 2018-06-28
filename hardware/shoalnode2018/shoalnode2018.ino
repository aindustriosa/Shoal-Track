// -*- mode: C++ -*-
/*
 * ShoalNode for ShoalTrack2018 system
 * 
 * Description:
 * Sistema de adquisicion de datos por telemetria descentralizada. 
 * Sobre dispositivo ArduinoMini Pro (5v16Mhz) y Hardware de comunicacion RF430 SX1278 LoRa
 * Utiliza las librerias RadioHead para comunicacion con LoRa a traves de un protocolo mallado
 * Utiliza un protocolo propio (CardumeProtocol) para el envío de información.
 * GPS de la marca ublox (solo atraves del codigo binario) UbxGps
 * IMU MPU6050
 * presion: BMP280
 * temperatura: 1x ds18b20
 * Luz: 1xLDR
 * Voltage: ADC interno
 * Amperios: ADC interno
 */

// 
#include "config.h"
#include <Arduino.h>
#include <RH_RF95.h> //para cargar el hardware de comunicaicones LoRa
#include <CardumeLink.h>
#include "Statistic.h"

//sistema gps:
#include <GPSUbloxBinary.h>

//el sistema de IMU (163 bytes de RAM) 
#define FSR 2000
#include <MPU9250_I2C_SHTRK.h>
#include <I2Cdev_GY91_SHTRK.h> //library from Jeff Rowberg

//ssitema de presion //BMP280
#include <Wire.h>
#include <BMP280_I2C_SHTRK_minimal.h>


// Singleton instance of the radio driver (420 bytes de RAM y 5.4 Kb de FLASH)
RH_RF95 cardume_driver; 

//creamos el manager de comunicaicones: (827 bytes de RAM y 2.5 Kb de FLASH)
CardumeLink net_manager(cardume_driver, CARDUME_ADDRESS);// 

//creamos el enlaceGPS
//NAV-PVT (Navigation Position Velocity Time Solution)[p308]: iTOW, year, month, day, hour, min, sec, valid, 
//tAcc, nano, fixType, flags, reserved1, numSV, lon, lat, height, hMSL, hAcc, vAcc, velN, velE, velD, 
//gSpeed, heading, sAcc, headingAcc, pDOP, reserved2, reserved3.
GPSUbloxBinary gps(Serial);
uint32_t timeGPSref; // Hold the milliseond 


//Variables de la IMU:
static int status_ret;

BMP280_I2C_minimal bme;


//TIME slots shedeluer
static uint8_t status; //parasaber si algo va mal...
uint32_t timeNow=0; // Hold the milliseond value for now
uint32_t timerStore=0;   //El anterior valor del timer 
int8_t cycleTimerCount=0;

uint8_t counter_1sA = 8;
uint8_t counter_1sB = 8;
uint8_t counter_2sA = 16;
uint8_t counter_2sB = 16;
uint8_t counter_5s = 40;


//variables de comunicaciones:
static crdm_Keys_t sh_keys ={ 0,"ASRS01",
                      {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       201, 202, 203, 204, 205, 206, 207, 208, 209, 210,211, 212, 213, 214, 215, 227},
                      {101,102,103,104,105,106,107,108},
                      {109, 110, 111, 112, 113, 114, 115, 116},
                      {0,0,0,0}
 };
Packet_Header_t  sh_header; //la parte dela cabezera y el tiempo

Packet_ShoalTrackReport_t sh_report; //los trama de sensorica
Packet_TraceRouteReport_t sh_traceroute; //los trama de traceroute

//Variables de la IMU:
int16_t temp_vector[3];

//memoria de datos adquiridos:
Statistic_int16t voltage;
Statistic_int16t current;
Statistic_int16t pressure;
Statistic_int16t ldr;

int16_t acc_global;
Statistic_int16t accx;
Statistic_int16t accy;
Statistic_int16t accz;

int16_t gyr_global;
Statistic_int16t gyrx;
Statistic_int16t gyry;
Statistic_int16t gyrz;
Statistic_int16t bearing;

////////////////////////////////////////////////////////////////////////////////
//MAIN SETUP
////////////////////////////////////////////////////////////////////////////////
void setup() {
    delay(500); //para estabilzar voltajes

    GPSPort.begin(GPS_BAUDRATE);
    delay(50);
    GPSPort.flush();
    
     //activo la red
    delay(100);
    status = net_manager.initialize(&sh_keys);
    if (status < 1){
        
    }
    
    timerStore=millis();
    timeNow=millis();
    cycleTimerCount = -1; // Reset case counter
    delay(20);
    
    //activo los leds de infromacion
    //FastLED.addLeds<WS2812B, DATA_PIN>(leds, NUM_LEDS);

    //initialize datas
    delay(100);
    sh_header.data.from=CARDUME_ADDRESS;
    sh_report.data.init();
    sh_traceroute.data.init();
    delay(100);
    
    //MPU9250
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Fastwire::setup(400,0);
    status_ret= mpu_init();
    status_ret = mpu_set_sensors(INV_XYZ_GYRO|INV_XYZ_ACCEL|INV_XYZ_COMPASS); 
    status_ret = mpu_set_gyro_fsr(IMU_FSR);
    status_ret = mpu_set_accel_fsr(IMU_ACCEL);
    status_ret = mpu_set_sample_rate(IMU_SAMPLE);
    mpu_get_power_state((unsigned char *)&status_ret);

    delay(100);
    mpu_calibrate_mag(5); //5 segundos de calibracion
    delay(100);
  

    //BMP280 [RAM: 41]
    bme.begin();
  
    //Confgure pinout
    pinMode(LDRPIN, INPUT);

    clear_values();
    delay(500);
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
             get_data_imu(); //8Hz
             break;
 
          case(1):
             get_data_power(); //8Hz
             break;
                        
          case(2):
             get_data_gps(); //8Hz
             //bloque retrasmision //se ejecuta cada 2 segundos
             if (counter_2sA == 0){
                send_report();
                clear_values(); //limpiio los datos
                
                counter_2sA = 16;
             }else{
                counter_2sA--;    
             }
            break;
                        
          case(3):
             get_data_imu(); //8Hz
             break;
                
          case(4):
             get_data_power(); //8Hz
             break;
                        
          case(5):
            //bloque retrasmision //se ejecuta cada 5 segundo
             if (counter_5s == 0){
                send_traceroute();
                
                counter_5s = 40;
             }else{
                counter_5s--;    
             }
            cycleTimerCount = -1; // Reset case counter, will be incremented to zero before switch statement
            break;
        }
    }

}

void clear_values(void){
  //reset values:
  voltage.clear();
  current.clear();
  pressure.clear();
  ldr.clear();
  acc_global=0;
  accx.clear();
  accy.clear();
  accz.clear();
  gyr_global= 0;
  gyrx.clear();
  gyry.clear();
  gyrz.clear();
  bearing.clear();
}

void get_data_imu(void){
  int16_t temp_var;
  mpu_get_accel_raw(&temp_vector[0],&temp_vector[1],&temp_vector[2]);
  accx.add(map(temp_vector[0],-32768, 32767, -2048, 2047)); //16 bits to int12_t
  if (accx.pop_stdev() > acc_global){ //paraver el valor maximo de la desviacion estandar
    acc_global = accx.pop_stdev();
  }
  
  //Serial.println(map(temp_vector[0],-32768, 32767, -2048, 2047));
  
   
  accy.add(map(temp_vector[1],-32768, 32767, -2048, 2047));  //16 bits to int12_t
  if (accy.pop_stdev() > acc_global){ //paraver el valor maximo
    acc_global = accy.pop_stdev();
  }
  
  accz.add(map(temp_vector[2],-32768, 32767, -2048, 2047)); //16 bits to int12_t
  if (accz.pop_stdev() > acc_global){ //paraver el valor maximo
    acc_global = accz.pop_stdev();
  }

  mpu_get_gyro_raw(&temp_vector[0],&temp_vector[1],&temp_vector[2]);
  gyrx.add(map(temp_vector[0],-32768, 32767, -2048, 2047)); //16 bits to int12_t
  if (gyrx.pop_stdev() > gyr_global){ //paraver el valor maximo
    gyr_global = gyrx.pop_stdev();
  }
  
  gyry.add(map(temp_vector[1],-32768, 32767, -2048, 2047)); //16 bits to int12_t
  if (gyry.pop_stdev() > gyr_global){ //paraver el valor maximo
    gyr_global = gyry.pop_stdev();
  }
  
  gyrz.add(map(temp_vector[2],-32768, 32767, -2048, 2047)); //16 bits to int12_t
  if (gyrz.pop_stdev() > gyr_global){ //paraver el valor maximo
    gyr_global = gyrz.pop_stdev();
  }
  
  bearing.add(map(mpu_get_compass_heading(),0,360, 0, 254)); //
  
  
  temp_vector[0] = (int16_t)bme.readPressure(); //presion en milibares(hPa)
  pressure.add(map(temp_vector[0],800, 1210, 0, 4095));// 800hPa-> 0Raw; 1210hPa->4095Raw
    
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
      sh_report.data.gps_longitude=gps.lon; 
      sh_traceroute.data.gps_latitude=gps.lat; 
      sh_report.data.gps_latitude=gps.lat; 
      
      //ahora la precision de la medida
      if (gps.fixType<2){
          sh_traceroute.data.gps_precision=1;
          sh_report.data.gps_precision=1;
      }else{
          
          if (gps.hAcc/1000<2){          //High
              sh_traceroute.data.gps_precision =7; 
              sh_report.data.gps_precision =7; 
          } else if (gps.hAcc/1000<10){  //HighLow
              sh_traceroute.data.gps_precision =6;
              sh_report.data.gps_precision =6; 
          }else if (gps.hAcc/1000<25){   //Medium
              sh_traceroute.data.gps_precision =5;
              sh_report.data.gps_precision =5; 
          }else if (gps.hAcc/1000<50){   //MediumLow
              sh_traceroute.data.gps_precision =4;
              sh_report.data.gps_precision =4; 
          }else if (gps.hAcc/1000<100){   //Low
              sh_traceroute.data.gps_precision =3;
              sh_report.data.gps_precision =3; 
          }else if (gps.hAcc/1000>100){   //LowLow
              sh_traceroute.data.gps_precision =2;
              sh_report.data.gps_precision =2; 
          }
      }
      
      sh_traceroute.data.gps_itow=gps.iTOW;
      sh_report.data.gps_itow=gps.iTOW;
      sh_report.data.gps_heading =  (uint8_t)map((int)gps.headMot/ 100000.0, 0, 359, 0, 255);
      
    }
    
}

void get_data_power(void){
  //voltage:
  temp_vector[0]= analogRead(VOLTPIN);
  temp_vector[1]= analogRead(VOLTPIN);
  temp_vector[2]= analogRead(VOLTPIN);
  voltage.add(map(temp_vector[2],0, 1023, 0, 4095)); //A7 -> 16 bits to uint12_t
  
  //Amperes
  temp_vector[0]= analogRead(AMPPIN);
  temp_vector[1]= analogRead(AMPPIN);
  temp_vector[2]= analogRead(AMPPIN);
  current.add(map(temp_vector[2],0, 1023, -2048, 2047)); //A6 -> 16 bits to int12_t

  //Ligth
  temp_vector[0]= analogRead(LDRPIN);
  temp_vector[1]= analogRead(LDRPIN);
  temp_vector[2]= analogRead(LDRPIN);
  ldr.add(map(temp_vector[2],0, 1023, 0, 4095)); //A2 -> 16 bits to uint12_t
    
}

/////////////////////////////////////////////////////////////////////
/////TRANSMISSION FUNCTIONS/////////////////////////////////////////

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

void send_traceroute(void){
   sh_traceroute.data.next_hop = net_manager.get_nexthop(CARDUME_GATEWAY_ADDRESS);
   sh_traceroute.data.rssi = net_manager.get_rssi();
   
  //send report:
    sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
    sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
    save_sh_header();//Actualizo el TimeMark

    net_manager.send_Packet(CARDUME_ID_TRACEROUTE,
                             sh_header.msg,sh_traceroute.msg);
    //net_manager.relay_packet(CARDUME_ID_TRACEROUTE,
    //                         sh_header.msg,sh_traceroute.msg, GPSPort);
}

void send_report(void){
    sh_report.data.next_hop = net_manager.get_nexthop(CARDUME_GATEWAY_ADDRESS);
  
    sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
    sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
    save_sh_header();//Actualizo el TimeMark
    //coloco cada valor en la estructura de memoria:
    save_sh_report();
    
    net_manager.send_Packet(CARDUME_ID_SHOALTRACK,
                             sh_header.msg,sh_report.msg);
}


void save_sh_report(void){
    uint8_t temp_var;
    sh_report.data.voltage_batt_avg = (uint16_t)voltage.average();
    temp_var = (uint8_t)map(voltage.pop_stdev(), 0, 1023, 0, 63);
    sh_report.data.voltage_batt_std_A = temp_var>>4;
    sh_report.data.voltage_batt_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.amperage_avg = current.average();
    temp_var = (uint8_t)map(current.pop_stdev(), 0, 1023, 0, 63);
    sh_report.data.amperage_std_A = temp_var>>4;
    sh_report.data.amperage_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.pressure_ext_avg = (uint16_t)pressure.average();
    temp_var = (uint8_t)map(pressure.pop_stdev(), 0, 1023, 0, 63);
    sh_report.data.pressure_ext_std_A = temp_var>>4;
    sh_report.data.pressure_ext_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.ligth_avg = (uint16_t)ldr.average();
    temp_var = (uint8_t)map(ldr.pop_stdev(), 0, 1023, 0, 63);
    sh_report.data.ligth_std_A = temp_var>>4;
    sh_report.data.ligth_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    //factor multiplicatvivo:
    sh_report.data.acc_std_F=acc_global/1023; //0,1,2,4
    
    sh_report.data.accx_avg = accx.average();
    temp_var = (uint8_t)map(accx.pop_stdev()/(sh_report.data.acc_std_F+1), 0, 1023, 0, 63);
    sh_report.data.accx_std_A = temp_var>>4;
    sh_report.data.accx_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    
    sh_report.data.accy_avg = accy.average();
    temp_var = (uint8_t)map(accy.pop_stdev()/(sh_report.data.acc_std_F+1), 0, 1023, 0, 63);
    sh_report.data.accy_std_A = temp_var>>4;
    sh_report.data.accy_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.accz_avg=  accz.average();
    temp_var = (uint8_t)map(accz.pop_stdev()/(sh_report.data.acc_std_F+1), 0, 1023, 0, 63);
    sh_report.data.accz_std_A = temp_var>>4;
    sh_report.data.accz_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    //factor multiplicatvivo:
    sh_report.data.gyr_std_F=gyr_global/1023; //0,1,2,4
    
    sh_report.data.gyrx_avg=  gyrx.average();
    temp_var = (uint8_t)map(gyrx.pop_stdev()/(sh_report.data.gyr_std_F+1), 0, 1023, 0, 63);
    sh_report.data.gyrx_std_A = temp_var>>4;
    sh_report.data.gyrx_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.gyry_avg=  gyry.average();
    temp_var = (uint8_t)map(gyry.pop_stdev()/(sh_report.data.gyr_std_F+1), 0, 1023, 0, 63);
    sh_report.data.gyry_std_A = temp_var>>4;
    sh_report.data.gyry_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.gyrz_avg=  gyrz.average();
    temp_var = (uint8_t)map(gyrz.pop_stdev()/(sh_report.data.gyr_std_F+1), 0, 1023, 0, 63);
    sh_report.data.gyrz_std_A = temp_var>>4;
    sh_report.data.gyrz_std_B = temp_var&0x0f; //cojo la low 0b00001111
    
    sh_report.data.bearing_avg= (uint8_t)bearing.average();
    temp_var = (uint8_t)map(bearing.pop_stdev(), 0, 359, 0, 31);
    sh_report.data.bearing_std = temp_var;
}

/*
void send_report(void){

  //sh_header.data.year=18;
  //sh_header.data.month=6;
  //sh_header.data.day=19;
  //sh_header.data.hour=17;
  //sh_header.data.min=21;
  //sh_header.data.seg=54;
  
  //sh_report.data.gps_longitude = -88979889;
  //sh_report.data.gps_latitude = 423456776;
  
  //sh_report.data.gps_heading  = 56;
  //sh_report.data.gps_precision = 1;
  sh_report.data.next_hop = 68;
  
    sh_report.data.voltage_batt_avg = 1019;
    sh_report.data.voltage_batt_std_B = 4;
    sh_report.data.voltage_batt_std_A = 2;
    
    sh_report.data.amperage_avg = 999;
    sh_report.data.amperage_std_B = 5;
    sh_report.data.amperage_std_A = 1;
    
    sh_report.data.pressure_ext_avg = 1055;
    sh_report.data.pressure_ext_std_B = 3;
    sh_report.data.pressure_ext_std_A = 0;
    
    sh_report.data.ligth_avg= 876;
    sh_report.data.ligth_std_B= 2;
    sh_report.data.ligth_std_A= 1;
    
    sh_report.data.accx_avg = -23;
    sh_report.data.accx_std_B= 6;
    sh_report.data.accx_std_A= 1;
    
    sh_report.data.accy_avg = 28;
    sh_report.data.accy_std_B= 8;
    sh_report.data.accy_std_A= 2;
    
    sh_report.data.accz_avg = 516;
    sh_report.data.accz_std_B= 9;
    sh_report.data.accz_std_A= 0;
    
    sh_report.data.gyrx_avg = 800;
    sh_report.data.gyrx_std_B= 6;
    sh_report.data.gyrx_std_A= 1;
    
    sh_report.data.gyry_avg = 790;
    sh_report.data.gyry_std_B= 8;
    sh_report.data.gyry_std_A= 2;
    
    sh_report.data.gyrz_avg = 996;
    sh_report.data.gyrz_std_B= 9;
    sh_report.data.gyrz_std_A= 0;
    
    
    sh_report.data.bearing_avg= 120;
    sh_report.data.bearing_std= 20;

    //send report:
    sh_header.data.magik=CARDUME_ID_MAGICK_OPEN; //packet sin codificar
    sh_header.data.to=CARDUME_GATEWAY_ADDRESS; //lo envio al gateway
    save_sh_header();//Actualizo el TimeMark

    //GatewayPort.println("\nREPORT: ");
    net_manager.send_Packet(CARDUME_ID_SHOALTRACK,
                             sh_header.msg,sh_report.msg);

}
*/


