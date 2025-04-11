#!/bin/bash

ROOT_DISK_SPACE=$(df -h | awk '/nvme0n1p2/ {print $4}')
#HOME_DISK_SPACE=$(df -h | awk '/home/ {print $4}')

MEM_FREE=$(free -h | awk '/Mem:/ {print $7}')

CPU=$(top -b -n1 -d1 | awk '/%Cpu/ {print $2"u "$4"s"}')

BAT=$(upower -i $(upower -e | grep BAT) | awk -F: '/perc/ {gsub(" +",""); print $2}')

#printf "[🖤%s|/=%s|~=%s|M:%-5s|C:%-11s]" "$BAT" "$ROOT_DISK_SPACE" "$HOME_DISK_SPACE" "$MEM_FREE" "$CPU"
printf "[🖤%s|/=%s|M:%-5s|C:%-11s]" "$BAT" "$ROOT_DISK_SPACE" "$MEM_FREE" "$CPU"

