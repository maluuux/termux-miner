#!/bin/bash

# สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

# ฟังก์ชันแยกและแสดงข้อมูล Wallet
function show_wallet_info() {
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

  # อ่านข้อมูล Wallet
  FULL_USER=$(jq -r '.user' "$CONFIG_FILE")
  
  # แยกส่วน Wallet และ Worker name
  WALLET_ADDRESS=$(echo "$FULL_USER" | cut -d'.' -f1)
  WORKER_NAME=$(echo "$FULL_USER" | cut -d'.' -f2-)

  # แสดงผลแบบสวยงาม
  clear
  echo -e "${PURPLE}╔══════════════════════════════════════════════════╗"
  echo -e "║${CYAN}              💰 WALLET INFORMATION              ${PURPLE}║"
  echo -e "╠══════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Full User String:${NC}"
  echo -e "║   ${GREEN}$FULL_USER${NC}"
  echo -e "╠══════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Wallet Address:${NC}"
  echo -e "║   ${CYAN}$WALLET_ADDRESS${NC}"
  echo -e "║${YELLOW} Worker/Donation Name:${NC}"
  echo -e "║   ${BLUE}$WORKER_NAME${NC}"
  echo -e "╠══════════════════════════════════════════════════╣"
  echo -e "║${GREEN}        Information extracted successfully!      ${PURPLE}║"
  echo -e "╚══════════════════════════════════════════════════╝${NC}"
}

# เรียกใช้งานฟังก์ชัน
show_wallet_info
~/ccminer/ccminer -c ~/ccminer/config.json