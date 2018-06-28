//definicion de las variables prncipales

//Alias UASRT ports
#define GPSPort Serial // an alias to port GPS

//Cargo la configuracion predefinida para las tramas
#define CARDUME_PROTOCOL CARDUME_PROTOCOL_SHOALTRACK

#define CARDUME_ADDRESS 20
#define CARDUME_GATEWAY_ADDRESS 201


//HARDWARE CONFIGURE:
#define RH_ROUTER_MAX_MESSAGE_LEN 50

//GPS
#define GPS_BAUDRATE 9600


//LED identification
#define NUM_LEDS  4
#define DATA_PIN_LED  3

//LDR light
#define LDRPIN A2

//power:
#define VOLTPIN A7
#define AMPPIN A6

//IMU:
#define IMU_FSR 1000
#define IMU_ACCEL 4
#define IMU_SAMPLE 160

//Pressure:
#define BMP280_CALIBRATRION_NP 73

//temperature:
#define ONE_WIRE_BUS 4              //Se declara el pin donde se conectará la DATA
#define DS18B20_RESOLUTION 12

//LED MODE:
#define LED_MODE_PANIC 0
#define LED_MODE_SYSTEM_INIT_1 1
#define LED_MODE_SYSTEM_INIT_2 2
#define LED_MODE_SYSTEM_INIT_3 3
#define LED_MODE_SYSTEM_INIT_4 4
#define LED_MODE_SYSTEM_INIT_OK 5

