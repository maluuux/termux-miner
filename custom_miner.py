#!/usr/bin/env python3
import subprocess
import re
import json
import sys
import os
from time import sleep

# โหลดการตั้งค่า
def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ ไม่พบไฟล์ config.json ใช้การตั้งค่าเริ่มต้น")
        return {
            "algorithm": "verus",
            "pool": "stratum+tcp://pool.url:port",
            "wallet": "YOUR_WALLET_ADDRESS",
            "password": "x"
        }

# ปรับแต่งการแสดงผล
def format_output(line):
    # ตรวจสอบ hashrate
    hashrate_match = re.search(r'(\d+\.\d+)\s*(kH|MH|GH)/s', line)
    if hashrate_match:
        speed, unit = hashrate_match.groups()
        units = {"kH": "กิโล", "MH": "เมกะ", "GH": "กิกะ"}
        return f"⚡ ความเร็ว: {speed} {units.get(unit, unit)}ฮาช/วินาที ⚡"
    
    # ตรวจสอบผลการขุด
    if 'accepted' in line:
        return f"✅ {line.strip()}"
    elif 'rejected' in line:
        return f"❌ {line.strip()}"
    
    return line.strip()

# ฟังก์ชันหลัก
def main():
    config = load_config()
    
    cmd = [
        './ccminer',
        '-a', config['algorithm'],
        '-o', config['pool'],
        '-u', config['wallet'],
        '-p', config['password']
    ]
    
    print(f"🚀 เริ่มขุดด้วยอัลกอริทึม: {config['algorithm']}")
    print(f"🔗 Pool: {config['pool']}")
    print("──────────────────────────")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            print(format_output(output))
        sleep(0.1)

if __name__ == "__main__":
    main()
