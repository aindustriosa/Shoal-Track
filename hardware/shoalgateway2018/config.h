//definicion de las variables prncipales

//Alias UASRT ports
#define GatewayPort Serial // an alias to PC
#define GPSPort Serial1 // an alias to port GPS
#define VaisalaPort Serial2 // an alias to sonda vaisala

//Cargo la configuracion predefinida para las tramas
#define CARDUME_PROTOCOL CARDUME_PROTOCOL_SHOALTRACK

#define CARDUME_ADDRESS 201
#define CARDUME_GATEWAY_ADDRESS 201


//HARDWARE CONFIGURE:
#define RH_ROUTER_MAX_MESSAGE_LEN 128

//LED status
#define NUM_LEDS  4
//#define LED_STATUS 3

//GPS
#define GPS_BAUDRATE 9600


//LED identification
#define NUM_LEDS  4
#define DATA_PIN_LED  3

//LDR light
#define LDRPIN A0



//LED MODE:
#define LED_MODE_PANIC 0
#define LED_MODE_SYSTEM_INIT_1 1
#define LED_MODE_SYSTEM_INIT_2 2
#define LED_MODE_SYSTEM_INIT_3 3
#define LED_MODE_SYSTEM_INIT_4 4
#define LED_MODE_SYSTEM_INIT_OK 5

