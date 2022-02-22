Hardware monitor by Robert Laszlo Szabo
---
lets you view things like temperature and clock speeds as they change
on your linux machine
Uses Linux sysfs and /proc to get most data
---
#TODO: add support for multiple GPUs/CPUs
#TODO: add support for non-nvidia GPUs

Supports:
CPU, NVIDIA GPU (WITH NVIDIA DRIVER), RAM, MOTHERBOARD, BIOS

Designed to be viewed on the terminal, or sent to a json file

all docs created by this program are in /tmp/openhwmon_linux/

USAGE: python3 main.py -r (float)

(float) = time interval at which hardware data is written to manifest.json

read data from /tmp/openhwmon_linux/manifest.json


VIEWING IN TERMINAL:
USAGE: python3 TerminalWindow.py

shows data at 1 second intervals
