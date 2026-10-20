#!/bin/sh
set -eu
mkdir -p /journal /home/student/evidence /run/sshd /run/user/1000
chmod 700 /journal
chown 1000:1000 /home/student /home/student/evidence /run/user/1000
cp /app/stations/bashrc /home/student/.bashrc
chown 1000:1000 /home/student/.bashrc
if [ ! -s /journal/host_ed25519 ]; then ssh-keygen -q -t ed25519 -N '' -f /journal/host_ed25519; fi
python -m app.station_agent &
if [ "$LAB_STATION" = analyst ]; then
  /usr/sbin/sshd -e -f /app/stations/sshd-analyst.conf
  mkdir -p /home/student/.ssh
  chmod 700 /home/student/.ssh
  if [ ! -s /home/student/.ssh/id_ed25519 ]; then
    ssh-keygen -q -t ed25519 -N '' -f /home/student/.ssh/id_ed25519
  fi
  cp /home/student/.ssh/id_ed25519.pub /access/id_ed25519.pub
  cp /app/stations/ssh_config /home/student/.ssh/config
  chmod 600 /home/student/.ssh/config /home/student/.ssh/id_ed25519
  chmod 644 /access/id_ed25519.pub
  chown -R 1000:1000 /home/student/.ssh
  mkdir -p /tmp/.X11-unix
  chmod 1777 /tmp/.X11-unix
  setpriv --reuid=1000 --regid=1000 --init-groups Xtigervnc :1 -geometry 1280x800 -depth 24 -localhost -SecurityTypes None -rfbport 5901 -Log '*:stderr:20' &
  sleep 1
  setpriv --reuid=1000 --regid=1000 --init-groups dbus-run-session -- /app/stations/session.sh &
  exec /usr/bin/python3 -m websockify --web /usr/share/novnc 6080 127.0.0.1:5901
else
  exec /usr/sbin/sshd -D -e -f /app/stations/sshd_config
fi
