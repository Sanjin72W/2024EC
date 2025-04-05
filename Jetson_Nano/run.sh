#!/bin/bash

echo "123456" | sudo -S sudo sh -c 'echo 255 > /sys/devices/pwm-fan/target_pwm'
echo "123456" | sudo -S sudo chmod 777 /dev/ttyTHS1
cd Code
cd B
echo "123456" | sudo -S sudo python3 main.py


