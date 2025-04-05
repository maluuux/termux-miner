#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# โหลดการตั้งค่า
if [ -f ~/.config/ccminer/config.cfg ]; then
    source ~/.config/ccminer/config.cfg
else
    echo -e "${RED}Error: Config file not found. Run setup.sh first.${NC}"
    exit 1
fi

# ตรวจสอบการอัปเดต
echo -e "${GREEN}[+] Checking for updates...${NC}"
git fetch
if [ $(git rev-parse HEAD) != $(git rev-parse @{u}) ]; then
    echo -e "${GREEN}[+] Updating...${NC}"
    git pull
    chmod +x *.sh
fi

# เริ่มขุด
echo -e "${GREEN}[+] Starting CCminer...${NC}"
echo -e "${GREEN}Pool: $POOL${NC}"
echo -e "${GREEN}Wallet: $WALLET${NC}"
echo -e "${GREEN}Worker: $WORKER${NC}"

./ccminer -a verus -o $POOL -u $WALLET.$WORKER -p x -t $(nproc --all)
