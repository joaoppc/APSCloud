#!/bin/sh

git clone https://github.com/joaoppc/APSCloud
apt-get install software-properties-common -y
apt-add-repository universe
apt-get update
apt-get install python-pip -y
pip install Flask 
pip install flask_restful 
pip install flask_httpauth
pip install pyrebase
cd /APSCloud
python serverAPS.py