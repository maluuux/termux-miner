#!/bin/bash

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
  echo -e "${YELLOW}"
  echo " ██████╗ ██████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗ "
  echo "██╔════╝██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗"
  echo "██║     ██║     ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝"
  echo "██║     ██║     ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗"
  echo "╚██████╗╚██████╗██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║"
  echo " ╚═════╝ ╚═════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
  echo -e "${NC}"
  echo -e "${CYAN}=== VRSC Miner for Termux ===${NC}"
  echo -e "${BLUE}Version: 2.0 UI Edition${NC}"
  echo -e "${MAGENTA}Created by: Your Name${NC}"
  echo ""
}

# ฟังก์ชันแสดงเมนู
function show_menu() {
  echo -e "${GREEN}1. ${YELLOW}Start Mining"
  echo -e "${GREEN}2. ${YELLOW}Check Settings"
  echo -e "${GREEN}3. ${YELLOW}Edit Config"
  echo -e "${GREEN}4. ${YELLOW}View Stats"
  echo -e "${GREEN}0. ${RED}Exit${NC}"
  echo ""
}

# ฟังก์ชันตรวจสอบการตั้งค่า
function check_settings() {
  if [ ! -f "config.json" ]; then
    echo -e "${RED}Error: config.json not found!${NC}"
    create_default_config
  fi

  POOL=$(grep -oP '"pool":\s*"\K[^"]+' config.json)
  WALLET=$(grep -oP '"wallet":\s*"\K[^"]+' config.json)
  WORKER=$(grep -oP '"worker":\s*"\K[^"]+' config.json)
  THREADS=$(grep -oP '"threads":\s*\K[0-9]+' config.json)

  echo -e "${CYAN}=== Current Settings ===${NC}"
  echo -e "${YELLOW}Pool: ${GREEN}$POOL${NC}"
  echo -e "${YELLOW}Wallet: ${GREEN}$WALLET${NC}"
  echo -e "${YELLOW}Worker: ${GREEN}$WORKER${NC}"
  echo -e "${YELLOW}Threads: ${GREEN}$THREADS${NC}"
  echo ""
}

# ฟังก์ชันสร้าง config เริ่มต้น
function create_default_config() {
  echo -e "${YELLOW}Creating default config file...${NC}"
  cat > config.json <<EOF
{
  "pool": "stratum+tcp://eu.luckpool.net:3956",
  "wallet": "YOUR_WALLET_ADDRESS_HERE",
  "worker": "termux-$(date +%s | tail -c 4)",
  "threads": 2
}
EOF
  echo -e "${GREEN}Config file created. Please edit it with your details.${NC}"
}

# ฟังก์ชันแก้ไข config
function edit_config() {
  if [ ! -f "config.json" ]; then
    create_default_config
  fi
  
  if command -v nano &> /dev/null; then
    nano config.json
  elif command -v vim &> /dev/null; then
    vim config.json
  elif command -v vi &> /dev/null; then
    vi config.json
  else
    echo -e "${RED}No text editor found. Please install nano/vim.${NC}"
    return
  fi
  
  echo -e "${GREEN}Config updated successfully!${NC}"
}

# ฟังก์ชันเริ่มการขุด
function start_mining() {
  check_settings
  
  if [ "$WALLET" == "YOUR_WALLET_ADDRESS_HERE" ]; then
    echo -e "${RED}Error: Please set your VRSC wallet address in config.json${NC}"
    edit_config
    return
  fi

  echo -e "${CYAN}=== Starting Miner ===${NC}"
  echo -e "${YELLOW}Pool: ${GREEN}$POOL${NC}"
  echo -e "${YELLOW}Wallet: ${GREEN}$WALLET${NC}"
  echo -e "${YELLOW}Worker: ${GREEN}$WORKER${NC}"
  echo -e "${YELLOW}Threads: ${GREEN}$THREADS${NC}"
  echo ""
  echo -e "${MAGENTA}Press Ctrl+C to stop mining${NC}"
  echo ""

  ./ccminer -a verus -o "$POOL" -u "$WALLET.$WORKER" -p x -t "$THREADS"
}

# ฟังก์ชันหลัก
function main() {
  while true; do
    show_header
    show_menu
    
    read -p "Select an option [0-4]: " choice
    echo ""
    
    case $choice in
      1) start_mining ;;
      2) check_settings 
         read -p "Press [Enter] to continue..." ;;
      3) edit_config ;;
      4) echo -e "${YELLOW}Feature coming soon!${NC}"
         sleep 2 ;;
      0) echo -e "${GREEN}Goodbye!${NC}"
         exit 0 ;;
      *) echo -e "${RED}Invalid option!${NC}"
         sleep 1 ;;
    esac
  done
}

# ตรวจสอบไฟล์ ccminer
if [ ! -f "ccminer" ]; then
  show_header
  echo -e "${RED}Error: ccminer binary not found in current directory!${NC}"
  echo -e "Please make sure:"
  echo -e "1. You're in the correct directory"
  echo -e "2. CCminer binary is named 'ccminer'"
  echo -e "3. The file has execute permission (run: chmod +x ccminer)"
  exit 1
fi

# เริ่มโปรแกรม
main
