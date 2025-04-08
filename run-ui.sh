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
  echo " V e r u s    M i n e r"
  echo -e ""

  # ส่วนข้อมูล Wallet และ Worker แยกกันชัดเจน
  echo -e "${YELLOW}Wallet Address:${NC} ${GREEN}$WALLET_ADDRESS${NC}"
  echo -e "${YELLOW}Worker Name:${NC}    ${BLUE}$WORKER_NAME${NC}"
  echo -e ""

  # ส่วนการตั้งค่าการขุด
  echo -e "${YELLOW}Algorithm:${NC}     ${GREEN}$ALGO${NC}"
  echo -e "${YELLOW}Threads:${NC}       ${CYAN}$THREADS${NC}"
  echo -e "${YELLOW}Retry Pause:${NC}   ${BLUE}$RETRY_PAUSE seconds${NC}"
  # ส่วน Pools ที่เปิดใช้งาน
  echo -e ""

  jq -c '.pools[] | select(.disabled == 0)' "$CONFIG_FILE" | while read -r pool; do
    POOL_NAME=$(echo "$pool" | jq -r '.name')
    POOL_URL=$(echo "$pool" | jq -r '.url')
    POOL_TIMEOUT=$(echo "$pool" | jq -r '.timeout')

    echo -e "${YELLOW}Pool Name:${NC}    ${GREEN}$POOL_NAME${NC}"
    echo -e "${CYAN}URL:${NC}         ${BLUE}$POOL_URL${NC}"
    echo -e "${BLUE}Timeout:${NC}     ${GREEN}$POOL_TIMEOUT seconds${NC}"
    echo -e ""
  done

  # ส่วน Pools ที่ปิดการใช้งาน
  DISABLED_COUNT=$(jq '[.pools[] | select(.disabled == 1)] | length' "$CONFIG_FILE")
  if [ "$DISABLED_COUNT" -gt 0 ]; then
    echo -e "${RED}=== DISABLED POOLS ($DISABLED_COUNT) ==="
    echo -e ""

    jq -c '.pools[] | select(.disabled == 1)' "$CONFIG_FILE" | while read -r pool; do
      POOL_NAME=$(echo "$pool" | jq -r '.name')
      echo -e "${RED}$POOL_NAME${NC}"
    done

    echo -e ""
  fi
  # ดีเลย์เป็นเวลา 5 วินาที
  sleep 10

}

# เรียกใช้งานฟังก์ชัน
show_simple_miner_info
