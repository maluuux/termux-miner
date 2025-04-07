#!/bin/bash
pkg update -y && pkg upgrade -y
pkg install -y python git libuv openssl hwloc

echo "📥 ดาวน์โหลด ccminer"
git clone https://github.com/[USER]/ccminer
cd ccminer-termux

chmod +x ccminer custom_miner.py

echo "🛠️ สร้างไฟล์ config (แก้ไขข้อมูลก่อนใช้)"
if [ ! -f "config.json" ]; then
    cp config.json
    echo "โปรดแก้ไขไฟล์ config.json ด้วยข้อมูลของคุณ!"
fi

echo "✅ ติดตั้งเสร็จสิ้น!"
echo "ใช้คำสั่ง: python custom_miner.py เพื่อเริ่มขุด"
