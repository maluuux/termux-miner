#!/bin/bash

echo "กำลังอัปเดต CCminer..."
wget -O  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget -O https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget -O https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh 
chmod +x ccminer start.sh
echo "อัปเดตเสร็จสมบูรณ์!"
