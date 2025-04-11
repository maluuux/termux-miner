#!/bin/bash
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json

#สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

function show_miner_info() {
  CONFIG_FILE="config.json"
  
  # ตรวจสอบไฟล์ config
  if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: config.json not found!${NC}"
    exit 1
  fi

  # ตรวจสอบ jq
  if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Installing jq...${NC}"
    pkg install -y jq > /dev/null 2>&1
  fi

  # อ่านข้อมูลหลัก
  FULL_USER=$(jq -r '.user' "$CONFIG_FILE")
  WALLET_ADDRESS=$(echo "$FULL_USER" | cut -d'.' -f1)
  WORKER_NAME=$(echo "$FULL_USER" | cut -d'.' -f2-)
  ALGO=$(jq -r '.algo' "$CONFIG_FILE")
  THREADS=$(jq -r '.threads' "$CONFIG_FILE")
  RETRY_PAUSE=$(jq -r '."retry-pause"' "$CONFIG_FILE")

  # แสดงผลแบบเรียบง่าย
echo -e "\033[0;36m"
echo "██╗   ██╗███████╗██████╗ ██╗   ██╗██████╗ "
echo "██║   ██║██╔════╝██╔══██╗██║   ██║██╔══██╗"
echo "██║   ██║█████╗  ██████╔╝██║   ██║██████╔╝"
echo "╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║██╔══██╗"
echo " ╚████╔╝ ███████╗██║  ██║╚██████╔╝██║  ██║"
echo "  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝"
echo "███╗   ███╗██╗███╗   ██╗███████╗██████╗ "
echo "████╗ ████║██║████╗  ██║██╔════╝██╔══██╗"
echo "██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝"
echo "██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗"
echo "██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║"
echo "╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
echo -e "\033[0m"
 echo ""
  echo -e "${YELLOW}เลขกระเป๋า💎 : ${GREEN}$WALLET_ADDRESS"
  echo -e "${YELLOW}ชื่อ miner👷  : ${RED}$WORKER_NAME"
  echo -e "${YELLOW}อัลกอริทึม⚙️    : ${GREEN}$ALGO"
  echo -e "${YELLOW}threads⚡   : ${CYAN}$THREADS"
  echo -e "${YELLOW}Retry Pause🔄 : ${BLUE}$RETRY_PAUSE"
  # แสดง Pools ที่ใช้งานอยู่
  echo -e "${CYAN}=== ACTIVE MINING POOLS ==="
  jq -c '.pools[] | select(.disabled == 0)' "$CONFIG_FILE" | while read -r pool; do
    POOL_NAME=$(echo "$pool" | jq -r '.name')
    POOL_URL=$(echo "$pool" | jq -r '.url')
    POOL_TIMEOUT=$(echo "$pool" | jq -r '.timeout')
    
    echo -e "${YELLOW}Pool: ${GREEN}$POOL_NAME"
    echo -e "${CYAN}URL: ${BLUE}$POOL_URL"
    echo -e "${YELLOW}Timeout: ${GREEN}$POOL_TIMEOUT"
    echo -e "\033[0m"
  done

#!/bin/bash
sleep 5
}

# เรียกใช้งานฟังก์ชัน
show_miner_info
 
 ~/ccminer/ccminer  -c ~/ccminer/config.json 
