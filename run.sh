# ดาวน์โหลดสคริปต์จาก GitHub
curl -L https://raw.githubusercontent.com/[username]/[repo]/[branch]/run.sh -o /data/data/com.termux/files/usr/bin/run

# ให้สิทธิ์การรัน
chmod +x /data/data/com.termux/files/usr/bin/run

# สร้างโฟลเดอร์ ccminer (ถ้ายังไม่มี)
mkdir -p ~/ccminer

# สร้างไฟล์ start.sh ตัวอย่าง (ถ้าคุณยังไม่มี)
echo '#!/bin/bash
echo "Starting miner..."
# ใส่คำสั่งเริ่ม miner ของคุณที่นี่' > ~/ccminer/start.sh
chmod +x ~/ccminer/start.sh
