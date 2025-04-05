#!/bin/bash
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
MAGENTA='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m' 
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
CONFIG=$(cat config.json)
POOL=$(echo $CONFIG | jq -r '.pool')
WALLET=$(echo $CONFIG | jq -r '.wallet')
WORKER=$(echo $CONFIG | jq -r '.worker')
THREADS=$(echo $CONFIG | jq -r '.threads')

# เริ่มการขุด
./ccminer -a verus -o "$POOL" -u "$WALLET.$WORKER" -p x -t "$THREADS"
