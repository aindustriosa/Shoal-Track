// CardumeLink.cpp
//
// Define Cardume Link Protocol 
// 
// Part of the ShoalTrack echosystem
//
// Author: Ignacio Gonzalez (igonzalez@cetmar.org)
// Copyright (C) 2018 Ignacio Gonzalez

#include "CardumeLink.h"
#include "CardumePacketHeartBeat.h"
#include "CardumePacketShoalTrackReport.h"
#include "CardumePacketTraceRouteReport.h"


////////////////////////////////////////////////////////////////////
// Constructors
CardumeLink::CardumeLink(RHGenericDriver& driver, uint8_t thisAddress) 
    : RHReliableDatagram(driver, thisAddress)
{
    
    memset(bufferRF, 0xBA, sizeof(bufferRF)); //inicializo a valores conocidos
}


/** Power on and prepare for general usage.
   This will activate the device, the cypher and inicialize vectors
*/
uint8_t CardumeLink::initialize(crdm_Keys_t *keydata) {

  if (!RHReliableDatagram::init()) {
    return 0;
  }
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then
  // you can set transmitter powers from 5 to 23 dBm:
  //  driver.setTxPower(23, false);
  // You can optionally require this module to wait until Channel Activity
  // Detection shows no activity on the channel before transmitting by setting
  // the CAD timeout to non-zero:
  //  driver.setCADTimeout(10000);
  RHReliableDatagram::setTimeout(CARDUME_MAX_TIME_WAIT);
  
  
  //sistema de checksum hash-cifrado:
  keys = keydata; //sincronizo las variables de claves
  
  poly1305.reset(keys->key8bytesIV); //reseteo el hash

  //sistema de cifrado:
  //encript DataPacket:
  cipher.setNumRounds(20); //para chacha20_256
  cipher.clear();
  cipher.setKey(keys->key32bytes, 32);//ajusto la clave
  cipher.setIV(keys->key8bytesIV, 8);
  cipher.setCounter(keys->counter_noce, 8);

  
  //inicializo el array subset: un puntero empezando en la posicion de la trama
  subsetPayload = &bufferRF[CARDUME_PAYLOAD_START]; 

  return 1;
}



//INTERNAL FUNCTIONS:

void CardumeLink::_decrypt_buffer (void) {
//desde donde hasta donde:
    
    //ajusto el counter:
    //decodifico el pacjkete con el nuevo counter
    cipher.setCounter(keys->counter_noce, 8);
    
    //cipher.decrypt(packetDecrypt, subsetPayload, subsetPayloadSize);
    

}

void CardumeLink::_add_hash (uint8_t bufferRF[]) {
    uint8_t count;
    poly1305.reset(keys->key8bytesIV); //inicializo el vector
    
    //hago hash del buffer
    poly1305.update(bufferRF, bufferRF[1]);
    
    //obtengo el hash token: nonce son los 16 primeros bytes del buffer
    //obtnego solo los 4 primeros bytes del hash
    poly1305.finalize(bufferRF, keys->token, 4);
    
    //meto hash en el buffer
    for (count = 0; count < 4; ++count) {
        bufferRF[bufferRF[1]-4+count]=keys->token[count];
    }
}

uint8_t CardumeLink::_check_hash (uint8_t bufferRF[]) {
    uint8_t hash[4];
    bufferRF[bufferRF[1]-4]=hash[0];
    bufferRF[bufferRF[1]-3]=hash[1];
    bufferRF[bufferRF[1]-2]=hash[2];
    bufferRF[bufferRF[1]-1]=hash[3];
    
    
    poly1305.reset(keys->key8bytesIV); //inicializo el vector
    
    //hago hash del buffer
    poly1305.update(bufferRF, bufferRF[1]);
    
    //obtengo el hash token: nonce son los 16 primeros bytes del buffer
    //obtnego solo los 4 primeros bytes del hash
    poly1305.finalize(bufferRF, keys->token, 4);
    
    return !memcmp(hash,keys->token, 4); //compara si son iguales
}

uint8_t CardumeLink::_get_packet_size (uint8_t packet_id) {
    switch (packet_id) {
    case CARDUME_ID_HEARTBEAT:
      return CARDUME_ID_HEARTBEAT_PACKETSIZE;
      break;
    case CARDUME_ID_TRACEROUTE:
      return CARDUME_ID_TRACEROUTE_PACKETSIZE;
      break;
    case CARDUME_ID_SHOALTRACK:
      return CARDUME_ID_SHOALTRACK_PACKETSIZE;
      break;
    case CARDUME_ID_METEOWIND:
      return CARDUME_ID_METEOWIND_PACKETSIZE;
      break;
    case CARDUME_ID_METEOTHP:
      return CARDUME_ID_METEOTHP_PACKETSIZE;
      break;
    case CARDUME_ID_METEORAIN:
      return CARDUME_ID_METEORAIN_PACKETSIZE;
      break;
    default:
      //si no encuentra nada, devuele un hertbeat..
      return CARDUME_ID_HEARTBEAT_PACKETSIZE;
  }
    
}


////////////////////////////////////////////////////////////////////
// Public methods for protocol

////////////////////////////////////////////////////////////////////
//envia la trama recivida a traves del RF..
uint8_t CardumeLink::send_Packet(uint8_t packet_id, uint8_t msg_header[],
                                                        uint8_t msg_payload[]){
    uint8_t sizeof_msg;
    
    //configuro el tamaño del packete final en el byte:1
    msg_header[1] = _get_packet_size(packet_id); //+el payload+hash
    sizeof_msg = msg_header[1]-CARDUME_SIZE_HEADERHASH; //menos el header y el hash
    
    //compongo el mensage: //copy struct header to variable array
    memcpy(&bufferRF[0], msg_header,CARDUME_ID_HEADER_PACKETSIZE); //primero el header
    //ahora el mesange del pakcet el tamaño total-tamaño de header y hash
    memcpy(&bufferRF[CARDUME_PAYLOAD_START],msg_payload, sizeof_msg);
    
    //añado el hash
    _add_hash(bufferRF);
    
    //cifro el payload si es necesario
    if (msg_header[0] ==CARDUME_ID_MAGICK_CYPHER){
        //ajusto el counter:  //codifico el pacjkete con el nuevo counter
        cipher.setCounter(keys->counter_noce, 8);
        //cifro el msg //lo meto directamente sbre el buffer desalida
        cipher.encrypt(subsetPayload, msg_payload, sizeof_msg); 
    }
    
    //lo envio
    
    return RHReliableDatagram::sendtoWait(bufferRF, 
                                      msg_header[CARDUME_ID_HEADER_LEN_POS],
                                      msg_header[CARDUME_ID_HEADER_TO_POS]);
}

//obtengo el salto necesario para alcanzar el destino
uint8_t CardumeLink::get_nexthop(uint8_t to_address){
    //si es a mi mismo:
    if (to_address==RHReliableDatagram::thisAddress()){
        return 0; //
    }
    //RoutingTableEntry* route = getRouteTo(to_address);
    //return route->next_hop;
    return to_address;
}

//obtengo el salto necesario para alcanzar el destino
int8_t CardumeLink::get_rssi(void){
    return (int8_t)RHReliableDatagram::_driver.lastRssi();
}


/////////////////////////////////////////////////////////////////
///PROCESS REQUEST FUNCTIONS
//Miro si hay una peticion esperando mi respuesta, relleno la respuesto con la estructura
//y obtengo el estado de la operacion
uint8_t CardumeLink::request_handle(void) {
  if (RHReliableDatagram::available())  {
    uint8_t packet_len;

    //espero respuesta  // Now wait for a reply from the server
    packet_len = CARDUME_MAX_PACKET_LEN; //para que entre toda la trama
    
    if (RHReliableDatagram::recvfromAckTimeout(bufferRF, 
        &packet_len,CARDUME_MAX_TIME_WAIT,&addr_from)) {
        
        //compruebo que es una trama valida:
        //Serial.print("\nMAgik: ");
        //Serial.println(bufferRF[0]);
        //magik packet:
        if( (bufferRF[0]!=CARDUME_ID_MAGICK_OPEN) && (bufferRF[0]!=CARDUME_ID_MAGICK_CYPHER)){
             return CARDUME_ERR_MAGIK; //fallo de paquete de inicioi
        }
        
        //miro siesta completa  packet:
        if( bufferRF[1]!=packet_len){
             return CARDUME_ERR_LEN; //fail tamño del packete
        }
        
        //a partir de aqui, la trama en principio es valida:
        if (bufferRF[CARDUME_ID_HEADER_TO_POS] ==RHReliableDatagram::thisAddress() ){ //si soy el destinatario:
            return CARDUME_MSG_TOME;
        } else if(bufferRF[CARDUME_ID_HEADER_TO_POS] ==CARDUME_NATOUT_ADDRESS) { // el destinatario es la salida al exterior
            return CARDUME_MSG_TOOUT;
        }else{
            return CARDUME_ERR_UNK;
        }
        
    }
    return CARDUME_ERR_TRASH; //no se ha recibido nada coherente
  }
  return CARDUME_ERR_NODATA; // no hay nada en el buffer
}



///obtengo el header del msg recibido
uint8_t CardumeLink::get_header(crdm_Header_t *dataheader, bool hashcypher=1) {
    
    //miro si esta codificada:
    if (bufferRF[0]==CARDUME_ID_MAGICK_CYPHER){
            //decodifico el packet:
            _decrypt_buffer();
    }
        
     //calculo hash:
     //if (hashcypher){
     //    if (_check_hash()){
     //     return 0; //fail!!
     //    }
    //}
    
    //copio parte del array en la estructura. 
    //OJO!! tiene que ser la estructura exacta!! (obtenida con request_handle)
    memcpy(&dataheader,bufferRF,sizeof(dataheader));
    
    //devuelvo el tipo de packete que he recibido:
    return bufferRF[9];
    
}

///obtengo la memoria en su estructura:
//lo tengo que hacer despues del header...
void CardumeLink::get_payload(void *datapayload) {
    
    //copio parte del array en la estructura. 
    //OJO!! tiene que ser la estructura exacta!! (obtenida con request_handle)
    memcpy(&datapayload,subsetPayload, bufferRF[1]-CARDUME_SIZE_HEADERHASH);
    
}

void CardumeLink::relay_packet_encode(uint8_t outBuff[], Stream & port){
    
    //configuro el tamaño del packete final
    outBuff[1] = _get_packet_size(outBuff[CARDUME_PAYLOAD_START]); //+el payload+hash
    
    memcpy(&bufferRF[0],outBuff, outBuff[1]); //copio al buffer de salida
    
     //añado el hash
    //_add_hash();
    
    //cifro el payload si es necesario
    if (bufferRF[0] ==CARDUME_ID_MAGICK_CYPHER){
        //ajusto el counter:  //codifico el pacjkete con el nuevo counter
        cipher.setCounter(keys->counter_noce, 8);
        //cifro el msg //lo meto directamente sbre el buffer desalida
        cipher.encrypt(&bufferRF[CARDUME_PAYLOAD_START],   
                                 &outBuff[CARDUME_PAYLOAD_START],
                                  outBuff[1]-CARDUME_ID_HEADER_PACKETSIZE-4); 
    }
    
    //lo envio
    port.write(bufferRF, outBuff[1]);
}

//envia la trama recivida RAW a traves del puerto serie que le meteaas..
uint8_t CardumeLink::relay_packet(uint8_t packet_id, uint8_t msg_header[],
                                                        uint8_t msg_payload[], Stream & port){
    uint8_t sizeof_msg;
    
    //configuro el tamaño del packete final en el byte:1
    msg_header[1] = _get_packet_size(packet_id); //+el payload+hash
    sizeof_msg = msg_header[1]-CARDUME_SIZE_HEADERHASH; //menos el header y el hash
    
    //compongo el mensage: //copy struct header to variable array
    memcpy(&bufferRF[0], msg_header,CARDUME_ID_HEADER_PACKETSIZE); //primero el header
    //ahora el mesange del pakcet el tamaño total-tamaño de header y hash
    memcpy(&bufferRF[CARDUME_PAYLOAD_START],msg_payload, sizeof_msg);
    
    //añado el hash
    _add_hash(bufferRF);
    
    
    //cifro el payload si es necesario
    if (msg_header[0] ==CARDUME_ID_MAGICK_CYPHER){
        //ajusto el counter:  //codifico el pacjkete con el nuevo counter
        cipher.setCounter(keys->counter_noce, 8);
        //cifro el msg //lo meto directamente sbre el buffer desalida
        cipher.encrypt(subsetPayload, msg_payload, sizeof_msg); 
    }
    
    //lo envio
    port.write(bufferRF, msg_header[1] );
    return 1;
}

void CardumeLink::relay_last_packet(Stream & port){
                                                            
    //lo renvio por el puerto 
    port.write(bufferRF, bufferRF[1]);

}
