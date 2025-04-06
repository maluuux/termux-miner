#!/bin/bash
# สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

# ฟังก์ชันแสดงสถานะ
function show_status() {
  # อ่านค่าจาก config.json
  POOL=$(jq -r '.pool' config.json)
  WALLET=$(jq -r '.wallet' config.json)
  WORKER=$(jq -r '.worker' config.json)
  THREADS=$(jq -r '.threads' config.json)
  MINER_NAME=$(jq -r '.miner_name // "VRSC Miner"' config.json)
  SHOW_WALLET=$(jq -r '.show_wallet // true' config.json)
  SHOW_THREADS=$(jq -r '.show_threads // true' config.json)

  clear
  echo -e "${PURPLE}╔══════════════════════════════════════════╗"
  echo -e "║${CYAN}           🚀 $MINER_NAME - REAL-TIME          ${PURPLE}║"
  echo -e "╠══════════════════════════════════════════╣"
  
  if [ "$SHOW_WALLET" = "true" ]; then
    echo -e "║${YELLOW} Wallet:${GREEN} $WALLET"
  fi
  
  echo -e "║${YELLOW} Pool:${GREEN} $POOL"
  echo -e "║${YELLOW} Worker:${GREEN} $WORKER"
  
  if [ "$SHOW_THREADS" = "true" ]; then
    echo -e "║${YELLOW} Threads:${GREEN} $THREADS"
  fi
  
  echo -e "║${YELLOW} Runtime:${GREEN} $RUNTIME minutes"
  echo -e "╠══════════════════════════════════════════╣"
  echo -e "║${CYAN} Hashrate:${BLUE} ${HASHRATE:-0} H/s"
  echo -e "║${CYAN} Accepted:${GREEN} ${ACCEPTED:-0} ${CYAN}Rejected:${RED} ${REJECTED:-0}"
  echo -e "║${CYAN} Last Share:${YELLOW} ${LAST_SHARE:-"None yet"}"
  echo -e "╠══════════════════════════════════════════╣"
  echo -e "║${RED} Press ${YELLOW}CTRL+C ${RED}to stop mining${PURPLE}             ║"
  echo -e "╚══════════════════════════════════════════╝${NC}"
}

# ตรวจสอบการตั้งค่า
if [ ! -f "config.json" ]; then
  echo -e "${RED}Error: config.json not found!${NC}"
  exit 1
fi

POOL=$(grep -oP '"pool":\s*"\K[^"]+' config.json)
WALLET=$(grep -oP '"wallet":\s*"\K[^"]+' config.json)
WORKER=$(grep -oP '"worker":\s*"\K[^"]+' config.json)
THREADS=$(grep -oP '"threads":\s*\K[0-9]+' config.json)

if [ "$WALLET" == "YOUR_WALLET_ADDRESS_HERE" ]; then
  echo -e "${RED}Error: Please set your VRSC wallet address in config.json${NC}"
  exit 1
fi

if [ ! -f "ccminer" ]; then
  echo -e "${RED}Error: ccminer binary not found!${NC}"
  exit 1
fi

# ตัวแปรเก็บสถานะ
ACCEPTED=0
REJECTED=0
START_TIME=$(date +%s)

# เริ่มกระบวนการขุด
{
  while read -r line; do
    # อัพเดทข้อมูลสถานะ
    if [[ $line == *"Accepted"* ]]; then
      ((ACCEPTED++))
      LAST_SHARE=$(date "+%H:%M:%S")
    elif [[ $line == *"Rejected"* ]]; then
      ((REJECTED++))
    elif [[ $line == *"Hashrate"* ]]; then
      HASHRATE=$(echo "$line" | grep -oE "[0-9]+\.[0-9]+")
    fi
    
    # คำนวณเวลารัน
    CURRENT_TIME=$(date +%s)
    RUNTIME=$(( (CURRENT_TIME - START_TIME) / 60 ))
    
    # แสดงสถานะ
    show_status
  done < <(./ccminer -a verus -o "$POOL" -u "$WALLET.$WORKER" -p x -t "$THREADS")
} || {
  echo -e "${RED}Miner stopped!${NC}"
}
~/ccminer/ccminer -c ~/ccminer/config.json
