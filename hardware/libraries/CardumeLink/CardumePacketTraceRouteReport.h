// -*- mode: C++ -*-
#ifndef _CardumePacketTraceRouteReport_H_
#define _CardumePacketTraceRouteReport_H_

//------------------------------------------------------
// @file CardumePacketTraceRouteReport.h
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

#define CARDUME_ID_TRACEROUTE_PACKETSIZE   28  // el header (8) + payload (16) + hash (4)

/// Cardume Packet desing:
struct crdm_TraceRouteReport_t {
    uint8_t packetid; //8 bits
    uint8_t next_hop; 
    int8_t rssi;
    uint8_t gps_precision;
    
    int32_t gps_longitude; //:
    int32_t gps_latitude; //:
    
    uint32_t gps_itow;     //32 bits
    
    void init() {
        packetid = CARDUME_ID_TRACEROUTE;
        next_hop:0;
        rssi=0;
        gps_precision=0;
        
        //Status System
        gps_longitude=0;
        gps_latitude=0;
        gps_itow=0;
       
    }

};

typedef union Packet_TraceRouteReport_t{
crdm_TraceRouteReport_t data;
uint8_t msg[sizeof(crdm_TraceRouteReport_t)];
};



#endif /* _CardumePacketTraceRouteReport_H_ */
    
