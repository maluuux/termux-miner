#!/bin/bash

# โหลดการตั้งค่า
CONFIG=$(cat config.json)
POOL=$(echo $CONFIG | jq -r '.pool')
WALLET=$(echo $CONFIG | jq -r '.wallet')
WORKER=$(echo $CONFIG | jq -r '.worker')
THREADS=$(echo $CONFIG | jq -r '.threads')

# เริ่มขุด
./ccminer -a verus -o $POOL -u $WALLET.$WORKER -p x -t $THREADS
