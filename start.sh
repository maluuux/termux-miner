#!/bin/bash
# โหลดการตั้งค่า
CONFIG=$(cat config.json)
POOL=$(echo $CONFIG | jq -r '.pool')
WALLET=$(echo $CONFIG | jq -r '.wallet')
WORKER=$(echo $CONFIG | jq -r '.worker')
THREADS=$(echo $CONFIG | jq -r '.threads')

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
