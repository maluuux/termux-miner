#!/bin/bash
# สีสำหรับการแสดงผล
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
NC='\033[0m'

# ฟังก์ชันแสดงข้อมูลทั้งหมด
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
  ALGO=$(jq -r '.algo' "$CONFIG_FILE")
  RETRY_PAUSE=$(jq -r '."retry-pause"' "$CONFIG_FILE")
  WALLE=${PURPLE}$(echo "$FULL_USER" | cut -d'.' -f1)
  WORKER_NAME=$(echo "$FULL_USER" | cut -d'.' -f2-)
  THREADS=$(jq -r '.threads' "$CONFIG_FILE")

  
  # แสดงผล
  clear
jq -c '.pools[] | select(.disabled == 0)' "$CONFIG_FILE" | while read -r pool; do
    POOL_NAME=$(echo "$pool" | jq -r '.name')
    POOL_URL=$(echo "$pool" | jq -r '.url')
    POOL_TIMEOUT=$(echo "$pool" | jq -r '.timeout')
  
    echo -e " ${YELLOW}$POOL_NAME${NC}"
    echo -e "   ${CYAN}URL:${GREEN} $POOL_URL${NC}"
    echo -e "   ${BLUE}Timeout:${GREEN} $POOL_TIMEOUT seconds${NC}"
  
  # ส่วนการตั้งค่าการขุด
  echo -e "${YELLOW} Algorithm:${GREEN} $ALGO${NC}"
  echo -e "${YELLOW} Threads:${CYAN} $THREADS${NC}"
  echo -e "${YELLOW} Retry Pause:${BLUE} $RETRY_PAUSE seconds${NC}"
   # ส่วนข้อมูล Wallet
  echo -e "${YELLOW} Wallet :${GREEN} $WALLET_ADDRESS${NC}"
  echo -e "${YELLOW} Name miner:${BLUE} $WORKER_NAME${NC}"
   
  
   
    echo -e "${CYAN}            🚀 VRSC MINER CONFIGURATION            ${NC}"
  done
  }

  while read -r line; do
    # กรองและประมวลผลแต่ละบรรทัด
    if [[ $line == *"Accepted"* ]]; then
      ((accepted++))
      last_share=$(date "+%Y-%m-%d %H:%M:%S")
      show_realtime_stats "$hashrate" "$accepted" "$rejected" "$(( ( $(date +%s) - start_time ) / 60 )" "$last_share"
    elif [[ $line == *"Rejected"* ]]; then
      ((rejected++))
      show_realtime_stats "$hashrate" "$accepted" "$rejected" "$(( ( $(date +%s) - start_time ) / 60 )" "$last_share"
    elif [[ $line == *"Hashrate"* ]]; then
      hashrate=$(echo "$line" | grep -oE "[0-9]+\.[0-9]+")
      show_realtime_stats "$hashrate" "$accepted" "$rejected" "$(( ( $(date +%s) - start_time ) / 60 )" "$last_share"
    elif [[ $line == *"New job"* ]]; then
      pool_url=$(echo "$line" | grep -oE "stratum[^ ]+")
      show_pool_info "Current Pool" "$pool_url" "${GREEN}ACTIVE${NC}"
    elif [[ $line == *"error"* || $line == *"failed"* ]]; then
      show_system_message "$line" "error"
    elif [[ $line == *"warning"* ]]; then
      show_system_message "$line" "warning"
    fi
  done
}
# เรียกใช้งานฟังก์ชัน
show_miner_info

~/ccminer/ccminer -c ~/ccminer/config.json
