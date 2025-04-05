#!/bin/bash

# ข้ามขั้นตอนดาวน์โหลดถ้ามีไฟล์ ccminer อยู่แล้ว
if [ -f "ccminer" ]; then
    echo "พบไฟล์ ccminer ที่มีอยู่แล้ว กำลังข้ามการดาวน์โหลด..."
else
    echo "ไม่พบไฟล์ ccminer กรุณาวางไฟล์ไว้ในโฟลเดอร์นี้"
    exit 1
fi

# ติดตั้ง dependencies (จำเป็น)
pkg update -y
pkg install -y wget openssl libcurl

# ให้สิทธิ์การรัน
chmod +x ccminer

# ดาวน์โหลดไฟล์ตั้งค่าเริ่มต้น (ถ้าไม่มี)
if [ ! -f "config.txt" ]; then
    wget https://raw.githubusercontent.com/<username>/<repo>/main/configs/default_config.txt -O config.txt
fi

echo "✅ ติดตั้งเสร็จสิ้น! ใช้คำสั่ง ./run.sh เพื่อเริ่ม"
