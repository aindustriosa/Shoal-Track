// -*- mode: C++ -*-
#ifndef _CardumePacketMeteoReport_H_
#define _CardumePacketMeteoReport_H_

//------------------------------------------------------
// @file CardumePacketMeteoReport.h
// @version 1.0.0
//
// @section License
// Copyright (C) 2018, Ignacio Gonzalez

// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//

#define CARDUME_ID_METEOWIND_PACKETSIZE   26  // el header (8) + payload (14) + hash (4)
#define CARDUME_ID_METEOTHP_PACKETSIZE   20  // el header (8) + payload (8) + hash (4)
#define CARDUME_ID_METEORAIN_PACKETSIZE   30  // el header (8) + payload (18) + hash (4)


/// Cardume Packet Meteo
struct crdm_MeteoWindReport_t {
    uint8_t packetid;
    uint8_t seconds;
    
    uint16_t wind_direction_min;
    uint16_t wind_direction_avg;
    uint16_t wind_direction_max;
    uint16_t wind_speed_min;
    uint16_t wind_speed_avg;
    uint16_t wind_speed_max;

    void init() {
     packetid = CARDUME_ID_METEOWIND;
     
     seconds=3;

     wind_direction_min=0;
     wind_direction_avg=0;
     wind_direction_max=0;
     wind_speed_min=0;
     wind_speed_avg=0;
     wind_speed_max=0;
    }
}; 

typedef union Packet_MeteoWindReport_t{
crdm_MeteoWindReport_t data;
uint8_t msg[sizeof(crdm_MeteoWindReport_t)];
};

/// Cardume Packet Meteo
struct crdm_MeteoTHPReport_t {
    uint8_t packetid;
    
    uint8_t seconds;
    
    int16_t air_temperature;
    uint16_t relative_humidity;
    uint16_t air_pressure;

    void init() {
     packetid = CARDUME_ID_METEOTHP;
    
     seconds=3;
     
     air_temperature=0;
     relative_humidity=0;
     air_pressure=0;
    }
}; 

typedef union Packet_MeteoTHPReport_t{
crdm_MeteoTHPReport_t data;
uint8_t msg[sizeof(crdm_MeteoTHPReport_t)];
};

/// Cardume Packet Meteo
struct crdm_MeteoRainReport_t {
    uint8_t packetid;
    
    uint8_t seconds;
    
    uint16_t rain_accumulation;
    uint16_t rain_duration;
    uint16_t rain_intensity;
    uint16_t hail_accumulation;
    uint16_t hail_duration;
    uint16_t hail_intensity;
    uint16_t rain_peak_intensity;
    uint16_t hail_peak_intensity;

    
    void init() {
    packetid = CARDUME_ID_METEORAIN;
    
    seconds=3;
    
     rain_accumulation=0;
     rain_duration=0;
     rain_intensity=0;
     hail_accumulation=0;
     hail_duration=0;
     hail_intensity=0;
     rain_peak_intensity=0;
     hail_peak_intensity=0;
    }
}; 

typedef union Packet_MeteoRainReport_t{
crdm_MeteoRainReport_t data;
uint8_t msg[sizeof(crdm_MeteoRainReport_t)];
};


#endif /* _CardumePacketMeteoReport_H_ */
    
