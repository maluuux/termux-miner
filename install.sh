#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== CCminer Auto-Install ===${NC}"

# ตรวจสอบ Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    echo -e "${RED}Error: สคริปต์นี้สำหรับ Termux เท่านั้น${NC}"
    exit 1
fi

# อัปเดตระบบ
echo -e "${GREEN}[+] อัปเดตแพ็คเกจระบบ...${NC}"
pkg update -y && pkg upgrade -y

# ติดตั้ง dependencies
echo -e "${GREEN}[+] ติดตั้ง dependencies...${NC}"
pkg install -y git wget proot cmake libuv openssl

# ดึงสคริปต์จาก GitHub
echo -e "${GREEN}[+] ดึงสคริปต์จาก GitHub...${NC}"
if [ -d "ccminer-auto-install" ]; then
    cd ccminer-auto-install
    git pull
else
    git clone https://github.com/yourusername/ccminer-auto-install.git
    cd ccminer-auto-install
fi

# ตั้งค่าสิทธิ์
chmod +x *.sh

# รันการตั้งค่า
echo -e "${GREEN}[+] เริ่มการตั้งค่า...${NC}"
./setup.sh
