#!/bin/bash

# Colors
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}[+] Updating CCminer...${NC}"

# อัปเดตสคริปต์
git pull origin main

# อัปเดต ccminer
if [ -f "ccminer" ]; then
    rm ccminer
fi

wget https://github.com/monkins1010/ccminer/releases/download/v3.9.0/ccminer-3.9.0-android-aarch64.tar.gz
tar -xvzf ccminer-3.9.0-android-aarch64.tar.gz
mv ccminer-3.9.0-android-aarch64/ccminer .
rm -rf ccminer-3.9.0-android-aarch64*

chmod +x ccminer *.sh

echo -e "${GREEN}Update completed!${NC}"
