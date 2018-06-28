// -*- mode: C++ -*-
#ifndef _CardumePacketHeartBeat_H_
#define _CardumePacketHeartBeat_H_

//------------------------------------------------------
// @file CardumePacketHeartBeat.h
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

#define CARDUME_ID_HEARTBEAT_PACKETSIZE   21  // el header (8) + payload (9) + hash (4)

/// Cardume Packet HeartBeat
struct crdm_heartbeat_t {
    uint8_t packetid;
    
    //Status System
    uint8_t structure_ext:4;
    uint8_t structure_int:4;
    uint8_t performance:4;
    uint8_t energy:4;
    uint8_t communication:4;
    uint8_t propulsion:4;
    uint8_t stability:4;
    uint8_t position:4;
    
    //Status Sensor
    uint8_t internal:4;
    uint8_t external:4;
    uint8_t meteorology:4;
    uint8_t oceanology:4;
    uint8_t visual:4;
    uint8_t sound:4;
    uint8_t samples:4;
    uint8_t other:4;
    
    void init() {
        packetid = 0x12;
        
        structure_ext = 0;
        structure_int=0;
        performance=0;
        energy = 0;
        communication = 0;
        propulsion = 0;
        stability= 0;
        position= 0;
        
        internal = 0;
        external=0;
        meteorology=0;
        oceanology = 0;
        visual = 0;
        sound = 0;
        samples= 0;
        other= 0;
    }
}; 


#endif /* _CardumePacketHeartBeat_H_ */
