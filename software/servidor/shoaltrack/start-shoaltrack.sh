#! /bin/bash
# Script de inicio de aplicacion PLACTOM en formato daemon

# por medio de WGSI:
uwsgi --ini /home/www-data/shoaltrack/shoaltrack-uwsgi-tcp.ini
