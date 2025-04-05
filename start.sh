#!/bin/bash

# สีสำหรับ UI
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# ฟังก์ชันแสดง UI ส่วนหัว
function show_header() {
  clear
  echo -e "${CYAN}"
  echo " ██╗   ██╗██████╗ ███████╗ ██████╗"
  echo " ██║   ██║██╔══██╗██╔════╝██╔════╝"
  echo " ██║   ██║██████╔╝███████╗██║     "
  echo " ╚██╗ ██╔╝██╔══██╗╚════██║██║     "
  echo "  ╚████╔╝ ██║  ██║███████║╚██████╗"
  echo "   ╚═══╝  ╚═╝  ╚═╝╚══════╝ ╚═════╝"
  echo -e "${NC}"
  echo -e "${MAGENTA}=== VRSC Auto Miner ===${NC}"
  echo -e "${YELLOW}Version: 2.1 Auto Mode${NC}"
  echo ""
}

# ตรวจสอบไฟล์ config
if [ ! -f "config.json" ]; then
  show_header
  echo -e "${YELLOW}Creating default config file...${NC}"
  cat > config.json <<EOF
{
  "pool": "stratum+tcp://eu.luckpool.net:3956",
  "wallet": "YOUR_WALLET_ADDRESS_HERE",
  "worker": "termux-$(date +%s | tail -c 4)",
  "threads": 2
}
EOF
  echo -e "${RED}Error: Please edit config.json with your VRSC wallet address!${NC}"
  exit 1
fi

# อ่านการตั้งค่า
POOL=$(grep -oP '"pool":\s*"\K[^"]+' config.json)
WALLET=$(grep -oP '"wallet":\s*"\K[^"]+' config.json)
WORKER=$(grep -oP '"worker":\s*"\K[^"]+' config.json)
THREADS=$(grep -oP '"threads":\s*\K[0-9]+' config.json)

# ตรวจสอบ wallet address
if [ "$WALLET" == "YOUR_WALLET_ADDRESS_HERE" ]; then
  show_header
  echo -e "${RED}Error: Please set your VRSC wallet address in config.json${NC}"
  exit 1
fi

# ตรวจสอบไฟล์ miner
if [ ! -f "ccminer" ]; then
  show_header
  echo -e "${RED}Error: Miner binary 'ccminer' not found!${NC}"
  echo -e "Please make sure:"
  echo -e "1. CCminer binary exists in this directory"
  echo -e "2. The file is named 'ccminer'"
  echo -e "3. It has execute permission (run: chmod +x ccminer)"
  exit 1
fi

# แสดงข้อมูลการขุด
show_header
echo -e "${GREEN}=== Mining Starting ===${NC}"
echo -e "${YELLOW}Pool: ${CYAN}$POOL${NC}"
echo -e "${YELLOW}Wallet: ${CYAN}$WALLET${NC}"
echo -e "${YELLOW}Worker: ${CYAN}$WORKER${NC}"
echo -e "${YELLOW}Threads: ${CYAN}$THREADS${NC}"
echo ""
echo -e "${MAGENTA}Press ${RED}Ctrl+C ${MAGENTA}to stop mining${NC}"
echo ""

# เริ่มการขุด
./ccminer -a verus -o "$POOL" -u "$WALLET.$WORKER" -p x -t "$THREADS"
