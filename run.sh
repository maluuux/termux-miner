#!/bin/bash

# สคริปต์สำหรับรัน CCminer บน Termux
# เวอร์ชัน 1.2 - ออกแบบสำหรับ ARM (Android)

clear
echo "======================================"
echo "  CCminer Launcher สำหรับ Termux"
echo "======================================"
echo

# ตรวจสอบไฟล์ config
CONFIG_FILE="config.txt"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[ERROR] ไม่พบไฟล์ config.txt"
    echo "กรุณาสร้างไฟล์ config.txt ก่อน โดยมีรูปแบบดังนี้:"
    echo "POOL=stratum+tcp://pool.example.com:3333"
    echo "WALLET=your_wallet_address"
    echo "WORKER=worker_name"
    echo "ALGO=verus"
    exit 1
fi

# โหลดการตั้งค่า
source $CONFIG_FILE

# ตรวจสอบพารามิเตอร์สำคัญ
if [ -z "$POOL" ] || [ -z "$WALLET" ] || [ -z "$ALGO" ]; then
    echo "[ERROR] การตั้งค่าไม่ครบถ้วน"
    echo "กรุณาตรวจสอบไฟล์ config.txt"
    exit 1
fi

# ตั้งค่า worker (ถ้าไม่ระบุ)
WORKER=${WORKER:-"termux"}

# ตรวจสอบไฟล์ ccminer
if [ ! -f "ccminer" ]; then
    echo "[ERROR] ไม่พบไฟล์ ccminer"
    echo "กรุณาวางไฟล์ ccminer สำหรับ ARM ไว้ในโฟลเดอร์นี้"
    exit 1
fi

# ให้สิทธิ์การรัน
chmod +x ccminer

# แสดงการตั้งค่า
echo "⚙️ การตั้งค่าปัจจุบัน:"
echo "--------------------------------------"
echo "Pool:      $POOL"
echo "Wallet:    $WALLET"
echo "Worker:    $WORKER"
echo "Algorithm: $ALGO"
echo "--------------------------------------"
echo

# ตรวจสอบสถาปัตยกรรม
echo "🔍 ตรวจสอบระบบ:"
ARCH=$(uname -m)
echo "- สถาปัตยกรรม CPU: $ARCH"
if [[ "$ARCH" != *"arm"* && "$ARCH" != *"aarch"* ]]; then
    echo "[WARNING] อาจมีปัญหากับ CPU ที่ไม่ใช่ ARM"
fi

# รัน miner
echo "🚀 กำลังเริ่มขุด..."
echo "กด Ctrl+C เพื่อหยุด"
echo "======================================"
echo

./ccminer -a $ALGO -o $POOL -u $WALLET.$WORKER -p x --quiet

# จบการทำงาน
echo
echo "======================================"
echo "❌ หยุดการขุด"
echo "ตรวจสอบ log ข้างต้นสำหรับข้อผิดพลาด (ถ้ามี)"
