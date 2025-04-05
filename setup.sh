#!/bin/bash

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

clear
echo -e "${GREEN}=== CCminer Setup ===${NC}"

# สร้างโฟลเดอร์ config ถ้ายังไม่มี
mkdir -p ~/.config/ccminer

# ตรวจสอบว่ามี config เก่าหรือไม่
if [ -f "~/.config/ccminer/config.cfg" ]; then
    source ~/.config/ccminer/config.cfg
else
    WALLET=""
    WORKER="android-$(date +%s | tail -c 4)"
    POOL="stratum+tcp://eu.luckpool.net:3956"
fi

# รับข้อมูลจากผู้ใช้
read -p "Enter VRSC Wallet Address [$WALLET]: " input_wallet
WALLET=${input_wallet:-$WALLET}

read -p "Enter Worker Name [$WORKER]: " input_worker
WORKER=${input_worker:-$WORKER}

read -p "Enter Mining Pool [$POOL]: " input_pool
POOL=${input_pool:-$POOL}

# บันทึกการตั้งค่า
echo "WALLET=\"$WALLET\"" > ~/.config/ccminer/config.cfg
echo "WORKER=\"$WORKER\"" >> ~/.config/ccminer/config.cfg
echo "POOL=\"$POOL\"" >> ~/.config/ccminer/config.cfg

# ดาวน์โหลด ccminer ถ้ายังไม่มี
if [ ! -f "ccminer" ]; then
    echo -e "${GREEN}[+] Downloading CCminer...${NC}"
    wget https://github.com/monkins1010/ccminer/releases/download/v3.9.0/ccminer-3.9.0-android-aarch64.tar.gz
    tar -xvzf ccminer-3.9.0-android-aarch64.tar.gz
    mv ccminer-3.9.0-android-aarch64/ccminer .
    rm -rf ccminer-3.9.0-android-aarch64*
fi

chmod +x ccminer

echo -e "${GREEN}Setup Completed! Run './start.sh' to begin mining.${NC}"
