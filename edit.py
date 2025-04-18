import json
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    clear_screen()
    print("⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻")
    print("       ⚒️ MINER CONFIGURATION ⚒️")
    print("⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻⎻")

def create_config():
    show_header()
    
    # กำหนดค่าเริ่มต้น
    config = {
        "pools": [{
            "name": "VIPOR",
            "url": "",
            "timeout": 180,
            "disabled": 0
        }],
        "user": "",
        "pass": "x",
        "algo": "verus",
        "threads": 4,
        "cpu-priority": 1,
        "cpu-affinity": -1,
        "retry-pause": 10,
        "api-allow": "192.168.1.0/255",
        "api-bind": "0.0.0.0:1001"
    }

    print("📌 กรอกข้อมูลการตั้งค่า\n")
    
    # รับข้อมูล Pool
    print("--- Pool Settings ---")
    config["pools"][0]["url"] = input("🔗 Pool URL (เช่น stratum+tcp://sg.vipor.net:5040): ")
    config["pools"][0]["name"] = input("🏷️ ชื่อ Pool (เช่น SG-VIPOR): ") or "VIPOR"
    
    # รับข้อมูล Wallet
    print("\n--- Wallet Settings ---")
    wallet = input("💰 Wallet Address: ") or "RVKoEnxatHpb6NWWtHOWpkXJkZ5uEbPs1m"
    miner_name = input("🏷️ ชื่อ Miner (เช่น Y9-2018-04): ") or "my-miner"
    config["user"] = f"{wallet}.{miner_name}"
    
    # รับค่าประสิทธิภาพ
    print("\n--- Performance Settings ---")
    config["threads"] = int(input("⚡ จำนวน Threads (ดีฟอลต์ 4): ") or 4)
    
    # บันทึกไฟล์
    save_path = "./config.json"
    with open(save_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    # รัน Miner ทันที
    print("\n🚀 กำลังเริ่มโปรแกรมขุด...")
    os.system(f"./miner -c {save_path}")

if __name__ == "__main__":
    try:
        create_config()
    except KeyboardInterrupt:
        print("\n❌ ยกเลิกการทำงาน")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️ เกิดข้อผิดพลาด: {e}")
        sys.exit(1)
