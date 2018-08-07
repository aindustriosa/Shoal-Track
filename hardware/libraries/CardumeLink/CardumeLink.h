// CardumeLink.h
//
// Author: Ignacio Gonzalez (igonzalez@cetmar.org)
// Copyright (C) 2018 Ignacio Gonzalez

#ifndef CARDUMELINK_H_
#define CARDUMELINK_H_

#include <RHReliableDatagram.h>
#include <Crypto.h>
#include <Poly1305.h>
#include <ChaCha.h>
#include <avr/pgmspace.h>

/////////////////////////////////////////////////////////////////////
/// \class CardumeLink CardumeLink.h <CardumeLink.h>
/// \brief CardumeLink Es una libreria para enviar datos estructurados a traves de la libreria RADIOHEAD.
/// Utiliza tecnicas de multisalto (red mallada) para enviar los datos, con deteccion automatica de rutas.

#if (CARDUME_DRIVER == CARDUME_DRIVER_RF95)
    #include <RH_RF95.h>
    #include <SPI.h>
#else
    #error You must define CARDUME_DRIVER
#endif

#ifndef CARDUME_INIT_ADDRESS
    #define CARDUME_INIT_ADDRESS 0x32
#endif

#define CARDUME_NATOUT_ADDRESS 0xff //la direccion de reenvio saliente.

////////////////////////////////////////
//TIME ON AIR REPORT:
//SF7: 170 ms
//SF9: 1100ms
//SF12 3000ms
//Variables de trasmision de datos RF:
#define CARDUME_MAX_TIME_WAIT 3000 //en milisegundos
#define CARDUME_TIME_SLOT_ONAIR 250 //El tiempo del slot en milisegundos
#define CARDUME_MAX_PACKET_LEN 80
#define CARDUME_MAX_PAYLOAD_LEN 64

#define CARDUME_SIZE_HEADERHASH 12 //el tamaño del header(8) mas el HASH(4)

#define CARDUME_PAYLOAD_START 8 //la posicion donde comienza el payload



//CODE ID PACKETS:
#define CARDUME_ID_MAGICK_OPEN   0x40 //es la @
#define CARDUME_ID_MAGICK_CYPHER 0x23 // es el #

#define CARDUME_ID_HEARTBEAT    0x30 // es el 0
#define CARDUME_ID_TRACEROUTE   0x40 // es el @
#define CARDUME_ID_ACKREPORT    0x41 // es el A
#define CARDUME_ID_SENDORDEN    0x42 // es el B

#define CARDUME_ID_SHOALTRACK   0x81 // es el
#define CARDUME_ID_METEOWIND    0x82 // es el B
#define CARDUME_ID_METEOTHP    0x83 // es el 
#define CARDUME_ID_METEORAIN    0x84 // es el 

//CODE  TRANSMISION:
#define CARDUME_ERR_NODATA 0
#define CARDUME_ERR_TRASH    1
#define CARDUME_ERR_MAGIK    2
#define CARDUME_ERR_LEN        3

#define CARDUME_MSG_TOME    10
#define CARDUME_MSG_TOOUT  20
#define CARDUME_ERR_UNK       30


#include "CardumePacketHeartBeat.h"
#include "CardumePacketTraceRouteReport.h"
#include "CardumePacketShoalTrackReport.h"
#include "CardumePacketMeteoReport.h"

#define CARDUME_ID_HEADER_PACKETSIZE  8
#define CARDUME_ID_HEADER_LEN_POS     1
#define CARDUME_ID_HEADER_FROM_POS  2
#define CARDUME_ID_HEADER_TO_POS       3
/// Cardume Packet Header
struct crdm_Header_t {
    uint8_t magik:8;

     //System Identifiacion
    uint8_t len:8;
    uint8_t from:8;
    uint8_t to:8;
     
    // los coloca en sentido inverso: anno,month,day...
     uint32_t seg:6;
     uint32_t min:6;
     uint32_t hour:5;
     
     uint32_t day:5;
     uint32_t month:4;
     uint32_t year:6;
    
}; 

typedef union Packet_Header_t {
   crdm_Header_t data;
   uint8_t msg [sizeof(crdm_Header_t)];
  };


struct crdm_Keys_t { 
    uint8_t id;
    uint8_t text[8];
    uint8_t key32bytes[32];
    uint8_t key8bytesIV[8];
    uint8_t counter_noce[8];
    uint8_t token[4];
};



class CardumeLink : public RHReliableDatagram
{
public:
        CardumeLink(RHGenericDriver& driver,
                              uint8_t thisAddress = CARDUME_INIT_ADDRESS);
        uint8_t initialize(crdm_Keys_t *keydata);
        
        uint8_t request_handle(void);
        
        uint8_t send_Packet(uint8_t packet_id, uint8_t msg_header[],
                                         uint8_t msg_payload[]);
        
        uint8_t get_nexthop(uint8_t to_address);
        int8_t get_rssi(void);
        bool available_Packet(void);
        
        uint8_t get_header(crdm_Header_t *dataheader, bool hashcypher);
        void get_payload(void *datapayload);
        
        //for gateway Node to PC:
        uint8_t relay_packet(uint8_t packet_id, uint8_t msg_header[],
                                         uint8_t msg_payload[], Stream & port);
        void relay_last_packet(Stream & port);
        
        void relay_packet_encode(uint8_t outBuff[], Stream & port);
        

    protected:

        /// Internal function that inspects messages being received and adjusts 

    private:
        uint8_t  _get_packet_size (uint8_t packet_id);
        void     _decrypt_buffer (void);
        void     _add_hash(uint8_t bufferRF[]);
        uint8_t  _check_hash (uint8_t bufferRF[]);
        
        Poly1305 poly1305; //para el hash cifrado
        ChaCha cipher; //class for cypher el payload RAM=186bytes
        crdm_Keys_t *keys; //es un puntero a la variable de claves
        
        /// The Driver we are to use
        uint8_t bufferRF[CARDUME_MAX_PACKET_LEN];
        uint8_t bufferCrypto[CARDUME_MAX_PAYLOAD_LEN];
        
        uint8_t *subsetPayload; //el array virtual donde esta el payload
        
        uint8_t addr_from = 0;

};

#endif
    
    
    
    
