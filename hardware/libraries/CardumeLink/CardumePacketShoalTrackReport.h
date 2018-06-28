// -*- mode: C++ -*-
#ifndef _CardumePacketShoalTrackReport_H_
#define _CardumePacketShoalTrackReport_H_

//------------------------------------------------------
// @file CardumePacketShoalTrackReport.h
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

#define CARDUME_ID_SHOALTRACK_PACKETSIZE   52  // el header (8) + payload (40) + hash (4)

/// Cardume Packet desing:
struct crdm_ShoalTrackReport_t {
    uint8_t packetid:8; //8 bits
    uint8_t next_hop:8; 
    
    uint8_t bearing_std:5; //3+5=8
    uint8_t gps_precision:3;
    uint8_t bearing_avg:8;
    
    uint8_t gps_heading:8; //para completar el pack de 32 bits padding
    
    uint8_t accz_std_A:2; //
    uint8_t accy_std_A:2; //
    uint8_t accx_std_A:2;  //
    uint8_t acc_std_F:2;
    
    uint8_t gyrz_std_A:2; //
    uint8_t gyry_std_A:2; //
    uint8_t gyrx_std_A:2;  //
    uint8_t gyr_std_F:2;
    
    uint8_t ligth_std_A:2;
    uint8_t pressure_ext_std_A:2; //
    uint8_t amperage_std_A:2; //
    uint8_t voltage_batt_std_A:2;  //
    
    
    uint16_t voltage_batt_avg:12; //12
    uint16_t voltage_batt_std_B:4;  //12+4=16
    
    int16_t amperage_avg:12;   // 12
    uint16_t amperage_std_B:4; //12+4=16
    
    uint16_t pressure_ext_avg:12; //
    uint16_t pressure_ext_std_B:4; //12+4=16
    
    uint16_t ligth_avg:12;
    uint16_t ligth_std_B:4;
    
    int16_t accx_avg:12;
    uint16_t accx_std_B:4;
    
    int16_t accy_avg:12;
    uint16_t accy_std_B:4;
    
    int16_t accz_avg:12;
    uint16_t accz_std_B:4;
    
    int16_t gyrx_avg:12;
    uint16_t gyrx_std_B:4;
    
    int16_t gyry_avg:12;
    uint16_t gyry_std_B:4;
    
    int16_t gyrz_avg:12;
    uint16_t gyrz_std_B:4;
    
    
    int32_t gps_longitude:32; //:28bits
    int32_t gps_latitude:32; //:28bits
    
    uint32_t gps_itow:32;     //32 bits
    
    void init() {
        packetid = CARDUME_ID_SHOALTRACK;
        next_hop:0;
        
        //Status System
        gps_longitude=0;
        gps_latitude=0;
        gps_heading=0;
        gps_itow=0;
        gps_precision=0;
        
        voltage_batt_avg=0;
        voltage_batt_std_B=0;
        voltage_batt_std_A=0;
        amperage_avg=0;
        amperage_std_B=0;
        amperage_std_A=0;

        pressure_ext_avg=0;
        pressure_ext_std_B=0;
        pressure_ext_std_A=0;

        ligth_avg=0;
        ligth_std_B=0;
        ligth_std_A=0;
        
        acc_std_F=0;
        accx_avg=0;
        accx_std_B=0;
        accx_std_A=0;
        accy_avg=0;
        accy_std_B=0;
        accy_std_A=0;
        accz_avg=0;
        accz_std_B=0;
        accz_std_A=0;
       
        gyr_std_F=0;
        gyrx_avg=0;
        gyrx_std_B=0;
        gyrx_std_A=0;
        gyry_avg=0;
        gyry_std_B=0;
        gyry_std_A=0;
        gyrz_avg=0;
        gyrz_std_B=0;
        gyrz_std_A=0;

        bearing_avg=0;
        bearing_std=0;
    }

};

typedef union Packet_ShoalTrackReport_t{
crdm_ShoalTrackReport_t data;
uint8_t msg[sizeof(crdm_ShoalTrackReport_t)];
};



#endif /* _CardumePacketShoalTrackReport_H_ */
    
