#!/bin/bash

# เปลี่ยนไปยังโฟลเดอร์ที่เก็บ start.sh
cd ~/ccminer  # แก้ไขพาธให้ตรงกับที่เก็บไฟล์ start.sh ของคุณ

# ตรวจสอบว่าไฟล์ start.sh มีอยู่
if [ -f "./start.sh" ]; then
    # ให้สิทธิ์การรัน (ถ้ายังไม่มี)
    chmod +x ./start.sh
    
    # รันสคริปต์
    ./start.sh
else
    echo "Error: start.sh not found in current directory"
    echo "Please make sure you're in the correct directory"
    exit 1
fi
