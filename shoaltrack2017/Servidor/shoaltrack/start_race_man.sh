#! /bin/bash
# Script de inicio de aplicacion PLACTOM en formato daemon

# por medio de WGSI:
python3 manage.py race_monitor 18-nocros-speed-race@serial:/dev/ttyACM0:115200 
