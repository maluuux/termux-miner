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
  FULL_USER=$(jq -r '.user' "$CONFIG_FILE")
  WALLET_ADDRESS=$(echo "$FULL_USER" | cut -d'.' -f1)
  WORKER_NAME=$(echo "$FULL_USER" | cut -d'.' -f2-)
  ALGO=$(jq -r '.algo' "$CONFIG_FILE")
  THREADS=$(jq -r '.threads' "$CONFIG_FILE")
  RETRY_PAUSE=$(jq -r '."retry-pause"' "$CONFIG_FILE")

  # แสดงผลแบบเรียบง่าย
  clear
  echo -e "${CYAN}=== VRSC MINER CONFIGURATION ==="
  echo -e "${YELLOW}Wallet Address: ${GREEN}$WALLET_ADDRESS"
  echo -e "${YELLOW}Worker Name: ${BLUE}$WORKER_NAME"
  echo -e "${YELLOW}Algorithm: ${GREEN}$ALGO"
  echo -e "${YELLOW}Threads: ${CYAN}$THREADS"
  echo -e "${YELLOW}Retry Pause: ${BLUE}$RETRY_PAUSE seconds"
  
  # แสดง Pools ที่ใช้งานอยู่
  echo -e "\n${CYAN}=== ACTIVE MINING POOLS ==="
  jq -c '.pools[] | select(.disabled == 0)' "$CONFIG_FILE" | while read -r pool; do
    POOL_NAME=$(echo "$pool" | jq -r '.name')
    POOL_URL=$(echo "$pool" | jq -r '.url')
    POOL_TIMEOUT=$(echo "$pool" | jq -r '.timeout')
    
    echo -e "${YELLOW}Pool: ${GREEN}$POOL_NAME"
    echo -e "  ${CYAN}URL: ${BLUE}$POOL_URL"
    echo -e "  ${YELLOW}Timeout: ${GREEN}$POOL_TIMEOUT seconds"
  done

  # แสดง Pools ที่ปิดการใช้งาน
  DISABLED_COUNT=$(jq '[.pools[] | select(.disabled == 1)] | length' "$CONFIG_FILE")
  if [ "$DISABLED_COUNT" -gt 0 ]; then
    echo -e "\n${RED}=== DISABLED POOLS ($DISABLED_COUNT) ==="
    jq -c '.pools[] | select(.disabled == 1)' "$CONFIG_FILE" | while read -r pool; do
      echo -e "${RED}$(echo "$pool" | jq -r '.name')"
    done
  fi

  echo -e "\n${GREEN}Config loaded successfully!${NC}"
}

# เรียกใช้งานฟังก์ชัน
show_miner_info
 
 ~/ccminer/ccminer  -c ~/ccminer/config.json 
