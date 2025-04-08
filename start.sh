#!/bin/bash

# สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

# ฟังก์ชันแสดงข้อมูลทั้งหมดแบบเรียบง่าย
function show_simple_miner_info() {
  CONFIG_FILE="config.json"
# ตั้งค่า path ของ config file
CONFIG_FILE="$HOME/config.json"

# ตรวจสอบไฟล์ config
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: config.json not found!${NC}"
    echo -e "${YELLOW}Please create config.json in your home directory first.${NC}"
    exit 1
fi

# ตรวจสอบ jq
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Installing jq...${NC}"
    pkg install -y jq > /dev/null 2>&1 || {
        echo -e "${RED}Failed to install jq!${NC}"
        exit 1
    }
fi

# อ่านค่าจาก config.json
POOL_URL=$(jq -r '.pools[0].url' "$CONFIG_FILE")
USER=$(jq -r '.user' "$CONFIG_FILE")
PASS=$(jq -r '.pass' "$CONFIG_FILE")
ALGO=$(jq -r '.algo' "$CONFIG_FILE")
THREADS=$(jq -r '.threads' "$CONFIG_FILE")

# ตรวจสอบค่าที่จำเป็น
if [[ -z "$POOL_URL" || -z "$USER" || -z "$ALGO" ]]; then
    echo -e "${RED}Invalid config: missing required fields!${NC}"
    echo -e "${YELLOW}Required fields: pools[0].url, user, algo${NC}"
    exit 1
fi
  # แสดงผลแบบเรียบง่าย
  echo -e "${CYAN}"
  echo " ██╗   ██╗███████╗██████╗ ██╗   ██╗███████╗"
  echo " ██║   ██║██╔════╝██╔══██╗██║   ██║██╔════╝"
  echo " ██║   ██║█████╗  ██████╔╝██║   ██║███████╗"
  echo " ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║   ██║╚════██║"
  echo "  ╚████╔╝ ███████╗██║  ██║╚██████╔╝███████║"
  echo "   ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
  echo " ███╗   ███╗██╗███╗   ██╗███████╗██████╗ "
  echo " ████╗ ████║██║████╗  ██║██╔════╝██╔══██╗"
  echo " ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝"
  echo " ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗"
  echo " ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║"
  echo " ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
  echo -e "${NC}"
  echo -e ""
  # แสดงข้อมูลการตั้งค่า
 echo -e "${GREEN}=== Mining Configuration ==="
 echo -e "Pool URL: ${POOL_URL}"
 echo -e "User: ${USER}"
 echo -e "Algorithm: ${ALGO}"
 echo -e "Threads: ${THREADS:-auto}${NC}"
  # ดีเลย์เป็นเวลา 5 วินาที
  sleep 10

}

# เรียกใช้งานฟังก์ชัน
show_simple_miner_info
 
 ~/ccminer/ccminer  -c ~/ccminer/config.json 
