#!/bin/bash

echo 'Prereq - python3 git'
CWD=$(pwd)
echo $CWD

cd ../../
git clone https://github.com/adafruit/Adafruit_Python_DHT.git &&
cd Adafruit_Python_DHT/ &&
INSTALLDIR=$(pwd)
sudo python3 setup.py install --force-pi &&
cd $CWD
echo "[IMP OUTPUT] Adafruit lib installed at $INSTALLDIR"
