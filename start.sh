#!/bin/bash

# ตรวจสอบว่าอยู่ในโฟลเดอร์ที่ถูกต้อง
if [ ! -f "ccminer" ]; then
    echo "Error: ccminer binary not found!"
    echo "Please run this script from the ccminer directory"
    exit 1
fi

# ตรวจสอบไฟล์ config
if [ ! -f "config.json" ]; then
    echo "Error: config.json not found!"
    echo "Creating default config..."
    cat > config.json <<EOF
{
    "pool": "stratum+tcp://eu.luckpool.net:3956",
    "wallet": "RVKoEnxatHeb6NWWtHVWpkPJkZ5uEbPs1m",
    "worker": "termux-worker",
    "threads": 2
}
EOF
    echo "Please edit config.json with your wallet address"
    exit 1
fi

# อ่านการตั้งค่าจาก config.json
POOL=$(grep -oP '"pool":\s*"\K[^"]+' config.json)
WALLET=$(grep -oP '"wallet":\s*"\K[^"]+' config.json)
WORKER=$(grep -oP '"worker":\s*"\K[^"]+' config.json)
THREADS=$(grep -oP '"threads":\s*\K[0-9]+' config.json)

# ตรวจสอบค่าที่จำเป็น
if [ -z "$WALLET" ] || [ "$WALLET" == "YOUR_WALLET_ADDRESS_HERE" ]; then
    echo "Error: Please set your VRSC wallet address in config.json"
    exit 1
fi

# เริ่มการขุด
echo "Starting CCminer with these settings:"
echo "Pool: $POOL"
echo "Wallet: $WALLET"
echo "Worker: $WORKER"
echo "Threads: $THREADS"
echo ""

./ccminer -a verus -o "$POOL" -u "$WALLET.$WORKER" -p x -t "$THREADS"
