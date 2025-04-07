#!/bin/bash

# สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

# ฟังก์ชันแสดงข้อมูล config
function show_config() {
  # อ่านค่าจาก config.json
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
  USER=$(jq -r '.user' "$CONFIG_FILE")
  ALGO=$(jq -r '.algo' "$CONFIG_FILE")
  THREADS=$(jq -r '.threads' "$CONFIG_FILE")
  RETRY_PAUSE=$(jq -r '."retry-pause"' "$CONFIG_FILE")
  API_ALLOW=$(jq -r '."api-allow"' "$CONFIG_FILE")
  API_BIND=$(jq -r '."api-bind"' "$CONFIG_FILE")

  # แสดงผล
  clear
  echo -e "${PURPLE}╔══════════════════════════════════════════════════╗"
  echo -e "║${CYAN}            ⚡ VRSC MINER CONFIGURATION            ${PURPLE}║"
  echo -e "╠══════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} User:${GREEN} $USER"
  echo -e "║${YELLOW} Algorithm:${GREEN} $ALGO"
  echo -e "║${YELLOW} Threads:${GREEN} $THREADS"
  echo -e "║${YELLOW} Retry Pause:${GREEN} $RETRY_PAUSE seconds"
  echo -e "║${YELLOW} API Access:${GREEN} $API_ALLOW"
  echo -e "║${YELLOW} API Bind:${GREEN} $API_BIND"
  echo -e "╠══════════════════════════════════════════════════╣"
  echo -e "║${CYAN}               AVAILABLE POOLS                ${PURPLE}║"
  echo -e "╠══════════════════════════════════════════════════╣"

  # แสดง pools
  jq -c '.pools[]' "$CONFIG_FILE" | while read -r pool; do
    NAME=$(echo "$pool" | jq -r '.name')
    URL=$(echo "$pool" | jq -r '.url')
    TIMEOUT=$(echo "$pool" | jq -r '.timeout')
    DISABLED=$(echo "$pool" | jq -r '.disabled')
    
    if [ "$DISABLED" = "0" ]; then
      STATUS="${GREEN}ACTIVE${NC}"
    else
      STATUS="${RED}DISABLED${NC}"
    fi
    
    echo -e "║ ${YELLOW}$NAME${NC}"
    echo -e "║   URL: ${CYAN}$URL${NC}"
    echo -e "║   Timeout: ${BLUE}$TIMEOUT${NC} seconds"
    echo -e "║   Status: $STATUS"
    echo -e "╠══════════════════════════════════════════════════╣"
  done

  echo -e "║${GREEN}        Config loaded successfully!         ${PURPLE}║"
  echo -e "╚══════════════════════════════════════════════════╝${NC}"

  # ดีเลย์พร้อมแสดงข้อความนับถอยหลัง
  delay_seconds=10
  echo "นับถอยลง $delay_seconds วินาที"
  for ((i=delay_seconds; i>=1; i--))
  do
  echo "$i..."
  sleep 1
  done
  echo "ทำงานต่อ!"
  
}

# เรียกใช้งานฟังก์ชัน
show_config

~/ccminer/ccminer -c ~/ccminer/config.json
