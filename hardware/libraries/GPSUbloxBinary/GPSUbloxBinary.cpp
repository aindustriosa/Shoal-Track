#include "GPSUbloxBinary.h"

GPSUbloxBinary::GPSUbloxBinary(Stream & serial) : _serial(serial)
{
    UbxHeader[0] = 0xB5;
    UbxHeader[1] = 0x62;
    
    //the size of nav_pvt packet: without checsum
    size = 98;
    carriagePosition=0;
}

void GPSUbloxBinary::resetChecksum(void){
    checksum[0] = 0;
    checksum[1] = 0;
}

void GPSUbloxBinary::calcChecksum(uint8_t newbyte){
        checksum[0] += newbyte;
        checksum[1] +=  checksum[0];
}

uint8_t GPSUbloxBinary::ready() {    
    while (_serial.available())
    {
        uint8_t c = _serial.read();
        
        // Estoy todavia encontrador el header
        if (carriagePosition < GPSUBLOXBINARY_HEADER_SIZE) {
            if (c == UbxHeader[carriagePosition])
            {
                carriagePosition++;
                //Serial.print("Found Header...\n"); 
            }
            // Reset if not
            else
            {
                carriagePosition = 0;
                //Serial.print("Reset Header... \n"); 
            }
            
        } else{ //he conseguido header, comienzo trama:
            //si comeinzo la trama, reseteo el checksum
            if (carriagePosition == GPSUBLOXBINARY_HEADER_SIZE){
                resetChecksum();
            }
            
            //Serial.print("Start Package... \n"); 
            switch (carriagePosition) {
                    case UBX_NAV_PVT_ITOW_OFFSET:
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        iTOW =  (uint32_t)buffer_rcv[0]<<24;
                        iTOW |= (uint32_t)buffer_rcv[1]<<16;
                        iTOW |= (uint32_t)buffer_rcv[2]<<8;
                        iTOW |= (uint32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        //Serial.print("Decode itow... \n"); 
                        
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        
                        break;
                    case UBX_NAV_PVT_YEAR_OFFSET:
                        buffer_rcv[0]= _serial.read();
                        
                        year = (uint16_t)buffer_rcv[0]<<8;
                        year |= (uint16_t)c;
                        
                        carriagePosition +=2;//he leido 2veces mas
                        //Serial.print("Decode year: ");
                        //Serial.println(c);
                        //Serial.println(buffer_rcv[0]);
                        
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[0]);
                        
                        break;
                    case UBX_NAV_PVT_MONTH_OFFSET:
                        month=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_DAY_OFFSET:
                        day=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_HOUR_OFFSET:
                        hour=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_MIN_OFFSET:
                        min=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_SEC_OFFSET:
                        sec=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_FIXTYPE_OFFSET:
                        fixType=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_NUMSV_OFFSET:
                        numSV=c;
                        carriagePosition +=1;//he leido 1veces mas
                        calcChecksum(c); //calculo el checksum:
                        break;
                    case UBX_NAV_PVT_LON_OFFSET:
                        int32_t   temp_val; 
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        lon =  (int32_t)buffer_rcv[0]<<24;
                        lon |= (int32_t)buffer_rcv[1]<<16;
                        lon |= (int32_t)buffer_rcv[2]<<8;
                        lon |= (int32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        break;
                    case UBX_NAV_PVT_LAT_OFFSET:
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        lat =  (int32_t)buffer_rcv[0]<<24;
                        lat |= (int32_t)buffer_rcv[1]<<16;
                        lat |= (int32_t)buffer_rcv[2]<<8;
                        lat |= (int32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        break;
                    case UBX_NAV_PVT_HEIGHT_OFFSET:
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        height =  (int32_t)buffer_rcv[0]<<24;
                        height |= (int32_t)buffer_rcv[1]<<16;
                        height |= (int32_t)buffer_rcv[2]<<8;
                        height |= (int32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        break;
                    case UBX_NAV_PVT_GSPEED_OFFSET:
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        gSpeed =  (int32_t)buffer_rcv[0]<<24;
                        gSpeed |= (int32_t)buffer_rcv[1]<<16;
                        gSpeed |= (int32_t)buffer_rcv[2]<<8;
                        gSpeed |= (int32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        break;
                    case UBX_NAV_PVT_HEADMOT_OFFSET:
                        buffer_rcv[2]= _serial.read();
                        buffer_rcv[1]= _serial.read();
                        buffer_rcv[0]= _serial.read();
                        
                        headMot =  (int32_t)buffer_rcv[0]<<24;
                        headMot |= (int32_t)buffer_rcv[1]<<16;
                        headMot |= (int32_t)buffer_rcv[2]<<8;
                        headMot |= (int32_t)c;
                        
                        carriagePosition +=4;//he leido 4veces mas
                        //Serial.print("Decode heading... \n"); 
                        //calculo el checksum:
                        calcChecksum(c);
                        calcChecksum(buffer_rcv[2]);
                        calcChecksum(buffer_rcv[1]);
                        calcChecksum(buffer_rcv[0]);
                        break;
                        
                    case UBX_NAV_PVT_CHECKSUM_OFFSET:
                        //comprobar checsum
                        if (checksum[0] == c){
                            c= _serial.read();
                            if (checksum[1] == c){
                                carriagePosition +=2;//he leido 2veces mas
                                return 1;
                            }
                        }else{
                            c= _serial.read();
                        }
                        
                        carriagePosition +=2;//he leido 2veces mas
                        //Serial.print("Decode checksum... \n"); 
                        return 0;
                        break;
                    default:
                        //si no hay variable, solo incremento
                         carriagePosition++;
                         calcChecksum(c);
            }
        }
        
    }
    
    //Serial.print("leave round... \n"); 
    return 0;
}
