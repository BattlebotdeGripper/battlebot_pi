#!/bin/bash


sudo ip link set can0 up type can bitrate 500000
# cd /home/battlebot/battlebot_pi/
# source venv/bin/activate
# python run/control.py

source /home/battlebot/battlebot/battlebot_pi/venv/bin/activate
python /home/battlebot/battlebot/battlebot_pi/run/control.py
