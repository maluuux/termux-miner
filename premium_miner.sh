#!/bin/bash

# สีสำหรับการแสดงผลระดับ Premium
BLACK='\033[0;30m'
RED='\033[1;38;5;196m'
GREEN='\033[1;38;5;46m'
YELLOW='\033[1;38;5;226m'
BLUE='\033[1;38;5;39m'
PURPLE='\033[1;38;5;129m'
CYAN='\033[1;38;5;51m'
WHITE='\033[1;38;5;255m'
NC='\033[0m'

# Gradient Colors
GOLD1='\033[1;38;5;220m'
GOLD2='\033[1;38;5;214m'
GOLD3='\033[1;38;5;208m'

# ฟังก์ชันแสดง Header แบบ Premium
function show_premium_header() {
  clear
  echo -e "${GOLD1}╔══════════════════════════════════════════════════════════╗"
  echo -e "║${GOLD2}   ██████╗ ██████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗   ${GOLD1}║"
  echo -e "║${GOLD3}  ██╔════╝██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗  ${GOLD1}║"
  echo -e "║${GOLD2}  ██║     ██║     ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝  ${GOLD1}║"
  echo -e "║${GOLD3}  ██║     ██║     ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗  ${GOLD1}║"
  echo -e "║${GOLD2}  ╚██████╗╚██████╗██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║  ${GOLD1}║"
  echo -e "║${GOLD3}   ╚═════╝ ╚═════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ${GOLD1}║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${CYAN}           V E R U S   P R E M I U M   E D I T I O N         ${GOLD1}║"
  echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
}

# ฟังก์ชันแสดงสถิติแบบเรียลไทม์
function show_realtime_stats() {
  local hashrate=$1
  local accepted=$2
  local rejected=$3
  local runtime=$4
  local last_share=$5
  
  echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗"
  echo -e "║${WHITE}                     REAL-TIME STATISTICS                   ${BLUE}║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Hashrate: ${GREEN}$hashrate H/s ${BLUE}║ ${YELLOW}Runtime: ${GREEN}$runtime minutes ${BLUE}           ║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Accepted Shares: ${GREEN}$accepted ${BLUE}║ ${YELLOW}Rejected Shares: ${RED}$rejected ${BLUE}          ║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Last Share Time: ${CYAN}$last_share ${BLUE}                                ║"
  echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
}

# ฟังก์ชันแสดงข้อมูล Pool
function show_pool_info() {
  local pool_name=$1
  local pool_url=$2
  local pool_status=$3
  
  echo -e "${PURPLE}╔══════════════════════════════════════════════════════════╗"
  echo -e "║${CYAN}                     CURRENT POOL INFO                     ${PURPLE}║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${YELLOW} Pool Name: ${GREEN}$pool_name ${PURPLE}                                ║"
  echo -e "║${YELLOW} Pool URL: ${BLUE}$pool_url ${PURPLE}║"
  echo -e "║${YELLOW} Status: $pool_status ${PURPLE}                                     ║"
  echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
}

# ฟังก์ชันแสดงข้อความระบบ
function show_system_message() {
  local message=$1
  local message_type=$2
  
  case $message_type in
    "error")
      echo -e "${RED}╔══════════════════════════════════════════════════════════╗"
      echo -e "║${WHITE} ! SYSTEM ALERT ! ${RED}                                      ║"
      echo -e "╠══════════════════════════════════════════════════════════╣"
      echo -e "║${WHITE} $message ${RED}"
      echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
      ;;
    "warning")
      echo -e "${YELLOW}╔══════════════════════════════════════════════════════════╗"
      echo -e "║${BLACK} ⚠ WARNING ⚠ ${YELLOW}                                        ║"
      echo -e "╠══════════════════════════════════════════════════════════╣"
      echo -e "║${WHITE} $message ${YELLOW}"
      echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
      ;;
    "success")
      echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗"
      echo -e "║${BLACK} ✓ SUCCESS ✓ ${GREEN}                                        ║"
      echo -e "╠══════════════════════════════════════════════════════════╣"
      echo -e "║${WHITE} $message ${GREEN}"
      echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
      ;;
    *)
      echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗"
      echo -e "║${WHITE} ℹ SYSTEM MESSAGE ℹ ${BLUE}                                  ║"
      echo -e "╠══════════════════════════════════════════════════════════╣"
      echo -e "║${WHITE} $message ${BLUE}"
      echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
      ;;
  esac
}

# ฟังก์ชันแสดงเมนู Premium
function show_premium_menu() {
  echo -e "${GOLD1}╔══════════════════════════════════════════════════════════╗"
  echo -e "║${GOLD2}                     P R E M I U M   M E N U                   ${GOLD1}║"
  echo -e "╠══════════════════════════════════════════════════════════╣"
  echo -e "║${GOLD3} 1. ${CYAN}Start Mining ${GOLD1}                                       ║"
  echo -e "║${GOLD3} 2. ${CYAN}Configure Pools ${GOLD1}                                    ║"
  echo -e "║${GOLD3} 3. ${CYAN}Performance Settings ${GOLD1}                               ║"
  echo -e "║${GOLD3} 4. ${CYAN}View Statistics ${GOLD1}                                    ║"
  echo -e "║${GOLD3} 5. ${CYAN}System Monitor ${GOLD1}                                     ║"
  echo -e "║${GOLD3} 6. ${CYAN}Advanced Options ${GOLD1}                                   ║"
  echo -e "║${GOLD3} 0. ${RED}Exit ${GOLD1}                                               ║"
  echo -e "╚══════════════════════════════════════════════════════════╝${NC}"
}

# ฟังก์ชันกรองและแสดงผล output ของ CCminer แบบ Premium
function premium_output_filter() {
  local hashrate=0
  local accepted=0
  local rejected=0
  local start_time=$(date +%s)
  local last_share="None yet"
  
  show_premium_header
  
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

# ตัวอย่างการใช้งาน
function start_premium_miner() {
  # อ่านการตั้งค่าจาก config.json
  CONFIG_FILE="config.json"
  POOL=$(jq -r '.pools[] | select(.disabled == 0) | .url' "$CONFIG_FILE" | head -n1)
  USER=$(jq -r '.user' "$CONFIG_FILE")
  THREADS=$(jq -r '.threads' "$CONFIG_FILE")
 }

# เริ่มโปรแกรม
start_premium_miner