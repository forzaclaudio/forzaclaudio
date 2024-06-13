#!/bin/bash

if [[ $1 -eq "1" ]]
then
    echo "Setting resolution to 640x480"
    WIDTH=640
    HEIGHT=480
elif [[ $1 -eq "2" ]]
then
    echo "Setting resolution to 960x720"
    WIDTH=960
    HEIGHT=720
elif [[ $1 -eq "3" ]]
then
    echo "Setting resolution to 1280x720"
    WIDTH=1280
    HEIGHT=720
elif [[ $1 -eq "4" ]]
then
    echo "Setting resolution to 1920x1080"
    WIDTH=1920
    HEIGHT=1080
else
  echo "Set resolution by providing the right selection 1=640×480, 2=960×720, 3=1280×720 (720p), 4=1920×1080 (1080p)"
  exit 0
fi

sudo rmmod v4l2loopback_dc
sudo insmod /lib/modules/`uname -r`/kernel/drivers/media/video/v4l2loopback-dc.ko width=$WIDTH height=$HEIGHT



