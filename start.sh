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
    echo "Error: $CONFIG_FILE not found!"
    exit 1
fi

# ตรวจสอบ jq
if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    pkg install -y jq > /dev/null 2>&1 || {
        echo "Failed to install jq!"
        exit 1
    }
fi

# อ่านค่าจาก config.json
POOL=$(jq -r '.pools[0].url' "$CONFIG_FILE")
USER=$(jq -r '.user' "$CONFIG_FILE")
PASS=$(jq -r '.pass' "$CONFIG_FILE")
ALGO=$(jq -r '.algo' "$CONFIG_FILE")
THREADS=$(jq -r '.threads' "$CONFIG_FILE")
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

# อ่านค่าจาก config.json
POOL=$(jq -r '.pools[0].url' "$CONFIG_FILE")
USER=$(jq -r '.user' "$CONFIG_FILE")
PASS=$(jq -r '.pass' "$CONFIG_FILE")
ALGO=$(jq -r '.algo' "$CONFIG_FILE")
THREADS=$(jq -r '.threads' "$CONFIG_FILE")
  # ดีเลย์เป็นเวลา 5 วินาที
  sleep 10

}

# เรียกใช้งานฟังก์ชัน
show_simple_miner_info
 
 ~/ccminer/ccminer  -c ~/ccminer/config.json 
