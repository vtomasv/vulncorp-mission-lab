#!/bin/sh
export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000
export XDG_CONFIG_HOME=/home/student/.config
xsetroot -solid '#e9edf3'
openbox --config-file /app/stations/openbox.xml &
xterm -title 'Terminal · Puesto de analisis' -geometry 112x30+50+60 -fa 'DejaVu Sans Mono' -fs 12 -bg '#f8fafc' -fg '#25384a' -e bash --rcfile /app/stations/bashrc -i &
wait
