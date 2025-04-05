#!/bin/bash

echo "กำลังอัปเดต CCminer..."
wget -O ccminer https://raw.githubusercontent.com/username/my-ccminer/main/ccminer
wget -O config.json https://raw.githubusercontent.com/username/my-ccminer/main/config.json
wget -O start.sh https://raw.githubusercontent.com/username/my-ccminer/main/start.sh
chmod +x ccminer start.sh
echo "อัปเดตเสร็จสมบูรณ์!"
