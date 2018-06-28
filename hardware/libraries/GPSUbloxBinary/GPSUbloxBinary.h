// CardumeLink.h
//
// Author: Ignacio Gonzalez (igonzalez@cetmar.org)
// Copyright (C) 2018 Ignacio Gonzalez

#ifndef GPSUBLOXBINARY_H_
#define GPSUBLOXBINARY_H_

#include <Arduino.h>
#include <stdint.h>
#include <Stream.h>

#define GPSUBLOXBINARY_HEADER_SIZE  2 // magic(2)+ IDs(2)+UNK(2)
#define GPSUBLOXBINARY_HEADER_PAYLOAD  4 // IDs(2)+UNK(2)
#define GPSUBLOXBINARY_CHECKSUM_SIZE  2 //


//NAV PVT defines offsets (2+4+x)
#define UBX_NAV_PVT_ITOW_OFFSET 6
#define UBX_NAV_PVT_YEAR_OFFSET 10
#define UBX_NAV_PVT_MONTH_OFFSET 12
#define UBX_NAV_PVT_DAY_OFFSET 13
#define UBX_NAV_PVT_HOUR_OFFSET 14
#define UBX_NAV_PVT_MIN_OFFSET 15
#define UBX_NAV_PVT_SEC_OFFSET 16

#define UBX_NAV_PVT_FIXTYPE_OFFSET 26 
#define UBX_NAV_PVT_NUMSV_OFFSET 29 
#define UBX_NAV_PVT_LON_OFFSET 30
#define UBX_NAV_PVT_LAT_OFFSET 34
#define UBX_NAV_PVT_HEIGHT_OFFSET 38

#define UBX_NAV_PVT_GSPEED_OFFSET 66
#define UBX_NAV_PVT_HEADMOT_OFFSET 70
#define UBX_NAV_PVT_CHECKSUM_OFFSET 98


struct ubx_nav_pvt {
    unsigned char   class_packet;      // class
    unsigned char   id_packet;      // class
    
    unsigned char   unkn1;      // Desconocido
    unsigned char   unkn2;      // Desconocido
    
// Type         Name           Unit     Description (scaling)
    unsigned long   iTOW;       // ms       GPS time of week of the navigation epoch. See the description of iTOW for 
                                //          details
    unsigned short  year;       // y        Year UTC
    unsigned char   month;      // month    Month, range 1..12 UTC
    unsigned char   day;        // d        Day of month, range 1..31 UTC
    unsigned char   hour;       // h        Hour of day, range 0..23 UTC
    unsigned char   min;        // min      Minute of hour, range 0..59 UTC
    unsigned char   sec;        // s        Seconds of minute, range 0..60 UTC
    char            valid;      // -        Validity Flags (see graphic below)
    unsigned long   tAcc;       // ns       Time accuracy estimate UTC
    long            nano;       // ns       Fraction of second, range -1e9..1e9 UTC
    unsigned char   fixType;    // -        GNSSfix Type, range 0..5
    char            flags;      // -        Fix Status Flags (see graphic below)
    char            flags2;     // -        Additional flags
    unsigned char   numSV;      // -        Number of satellites used in Nav Solution
    long            lon;        // deg      Longitude (1e-7)
    long            lat;        // deg      Latitude (1e-7)
    long            height;     // mm       Height above Ellipsoid
    long            hMSL;       // mm       Height above mean sea level
    unsigned long   hAcc;       // mm       Horizontal Accuracy Estimate
    unsigned long   vAcc;       // mm       Vertical Accuracy Estimate
    long            velN;       // mm/s     NED north velocity
    long            velE;       // mm/s     NED east velocity
    long            velD;       // mm/s     NED down velocity
    long            gSpeed;     // mm/s     Ground Speed (2-D)
    long            headMot;    // deg      Heading of motion 2-D (1e-5)
    unsigned long   sAcc;       // mm/s     Speed Accuracy Estimate
    unsigned long   headingAcc; // deg      Heading Accuracy Estimate (1e-5)
    unsigned short  pDOP;       // -        Position DOP (0.01)
    unsigned char   reserved1;  // -        Reserved
    unsigned char   reserved2;  // -        Reserved
    unsigned char   reserved3;  // -        Reserved
    unsigned char   reserved4;  // -        Reserved
    unsigned char   reserved5;  // -        Reserved
    unsigned char   reserved6;  // -        Reserved
    long            headVeh;    // deg      Heading of vehicle (2-D) (1e-5 )
    short           magDec;     // deg      Magnetic declination (1e-2)
    unsigned short  magAcc;     // deg      Magnetic declination accuracy (1e-2)
    
}; 



class GPSUbloxBinary
{
  public:
    GPSUbloxBinary(Stream & serial);
    uint8_t ready();
    
    //values:
    uint32_t   iTOW;       // ms       GPS time of week of the navigation epoch. 
    uint16_t  year;       // y        Year UTC
    uint8_t   month;      // month    Month, range 1..12 UTC
    uint8_t   day;        // d        Day of month, range 1..31 UTC
    uint8_t hour;       // h        Hour of day, range 0..23 UTC
    uint8_t   min;        // min      Minute of hour, range 0..59 UTC
    uint8_t   sec;        // s        Seconds of minute, range 0..60
    
    uint8_t   fixType;    // -        GNSSfix Type, range 0..5
    uint8_t   numSV;      // -        Number of satellites used in Nav Solution
    int32_t   lon;        // deg      Longitude (1e-7)
    int32_t   lat;        // deg      Latitude (1e-7)
    int32_t   height;     // mm       Height above Ellipsoid
    
    uint32_t   hAcc;       // mm       Horizontal Accuracy Estimate
    uint32_t   vAcc;       // mm       Vertical Accuracy Estimate
    
    int32_t     gSpeed;     // mm/s     Ground Speed (2-D)
    int32_t     headMot;    // deg      Heading of motion 2-D (1e-5)


  private:
    void resetChecksum(void);
    void calcChecksum(uint8_t newbyte);
    
    uint8_t UbxHeader[2];
    //ubx_nav_pvt payload; //
    uint8_t checksum[GPSUBLOXBINARY_CHECKSUM_SIZE]; //
    
    uint8_t buffer_rcv[3]; //un buffer para hacer cambio MSB->LSB
    

    // Class properties
    Stream &_serial;
    uint8_t size;
    uint8_t carriagePosition;
    

};

#endif
