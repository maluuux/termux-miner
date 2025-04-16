import subprocess
import re
import time
from datetime import datetime
import json
import os
import sys

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30
        self.config = self.load_config()
        self.last_difficulty = None
        self.last_update_time = None
        self.alert_messages = []
        self.running = True
        self.miner_data = {
            'hashrate': 0,
            'difficulty': 0,
            'accepted': 0,
            'rejected': 0,
            'connection': {
                'status': 'กำลังเชื่อมต่อ...',
                'pool': self.config.get('pools', ['ไม่ระบุ'])[0],
                'url': 'ไม่ระบุ'
            },
            'block': 0,
            'cpu_threads': {}
        }

    def clean_log_line(self, line):
        """ลบรหัสสีและคัดกรองข้อความสำคัญ"""
        # ลบ ANSI color codes
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        return clean_line.strip()

    def add_alert_message(self, message, alert_type='info'):
        """เพิ่มข้อความแจ้งเตือน"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.alert_messages.append(f"[{timestamp}] {message}")
        if len(self.alert_messages) > 3:
            self.alert_messages.pop(0)

    def load_config(self):
        """โหลดการตั้งค่าจากไฟล์ config"""
        default_config = {
            'wallet_address': 'ไม่ระบุ',
            'miner_name': 'ไม่ระบุ',
            'threads': 'ไม่ระบุ',
            'pools': ['ไม่ระบุ']
        }
        
        try:
            config_path = os.path.expanduser('~/config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.add_alert_message(f"โหลด config ไม่สำเร็จ: {str(e)}", 'error')
        
        return default_config

    def parse_miner_output(self, line):
        """ประมวลผลผลลัพธ์จาก miner"""
        line = self.clean_log_line(line)
        updated = False

        # ตรวจสอบข้อความสำคัญ
        if 'accepted' in line.lower() and 'rejected' in line.lower():
            try:
                parts = re.split(r'\s+', line)
                accepted = int(parts[parts.index('accepted:') + 1])
                rejected = int(parts[parts.index('rejected:') + 1])
                if accepted != self.miner_data['accepted'] or rejected != self.miner_data['rejected']:
                    self.miner_data['accepted'] = accepted
                    self.miner_data['rejected'] = rejected
                    updated = True
            except:
                pass

        # หาค่า hashrate
        hashrate_match = re.search(r'(\d+\.\d+)\s*H/s', line)
        if hashrate_match:
            hashrate = float(hashrate_match.group(1))
            if hashrate != self.miner_data['hashrate']:
                self.miner_data['hashrate'] = hashrate
                updated = True

        # หาค่า CPU threads
        cpu_thread_match = re.search(r'CPU T(\d+)\s*:\s*([\d.]+)\s*H/s', line)
        if cpu_thread_match:
            thread_num = int(cpu_thread_match.group(1))
            thread_hashrate = float(cpu_thread_match.group(2))
            self.miner_data['cpu_threads'][thread_num] = thread_hashrate
            updated = True

        # ตรวจสอบการเชื่อมต่อ
        if 'connected to' in line.lower():
            self.miner_data['connection']['status'] = '✅ เชื่อมต่อแล้ว'
            updated = True
        elif 'connecting to' in line.lower():
            self.miner_data['connection']['status'] = '🔄 กำลังเชื่อมต่อ...'
            updated = True

        return updated

    def format_hashrate(self, hashrate):
        """จัดรูปแบบ hashrate"""
        if hashrate >= 1000000:
            return f"{hashrate / 1000000:.2f} MH/s"
        elif hashrate >= 1000:
            return f"{hashrate / 1000:.2f} kH/s"
        return f"{hashrate:.2f} H/s"

    def display_dashboard(self):
        """แสดงผลข้อมูลบนหน้าจอ Termux"""
        # ล้างหน้าจอ
        print("\033[2J\033[H", end="")

        # สีสำหรับ Termux
        COLORS = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }

        # ส่วนหัว
        print(f"{COLORS['bold']}⚡ VRSC Miner Monitor ⚡{COLORS['reset']}")
        print(f"เวลา: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)

        # แสดงแจ้งเตือน
        if self.alert_messages:
            print(f"{COLORS['yellow']}แจ้งเตือน:{COLORS['reset']}")
            for msg in self.alert_messages[-2:]:
                print(f" {msg}")
            print("-" * 40)

        # สถานะการขุด
        runtime = int(time.time() - self.start_time)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        seconds = runtime % 60
        
        print(f"⏱️ เวลาทำงาน: {hours}:{minutes:02d}:{seconds:02d}")
        print(f"🔗 สถานะ: {self.miner_data['connection']['status']}")
        print(f"⚡ Hashrate: {self.format_hashrate(self.miner_data['hashrate'])}")
        print(f"📊 Shares: {self.miner_data['accepted']}/{self.miner_data['rejected']}")
        print("-" * 40)

        # แสดง CPU Threads
        print(f"{COLORS['bold']}CPU Threads:{COLORS['reset']}")
        if self.miner_data['cpu_threads']:
            max_hashrate = max(self.miner_data['cpu_threads'].values()) if self.miner_data['cpu_threads'] else 1
            for thread_num in sorted(self.miner_data['cpu_threads']):
                hashrate = self.miner_data['cpu_threads'][thread_num]
                bar_length = 10  # สั้นลงสำหรับหน้าจอเล็ก
                filled = int(round(hashrate / max_hashrate * bar_length))
                bar = '█' * filled + '-' * (bar_length - filled)
                
                if hashrate >= max_hashrate * 0.8:
                    color = COLORS['green']
                elif hashrate >= max_hashrate * 0.5:
                    color = COLORS['yellow']
                else:
                    color = COLORS['red']
                
                print(f"T{thread_num}: {color}{bar}{COLORS['reset']} {hashrate:.1f} H/s")
        else:
            print("กำลังโหลดข้อมูล CPU...")

    def run(self):
        try:
            process = subprocess.Popen(
                ["./ccminer"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.display_dashboard()

            while self.running:
                line = process.stdout.readline()
                if not line:
                    break
                    
                if self.parse_miner_output(line):
                    self.display_dashboard()

        except KeyboardInterrupt:
            print("\nกำลังปิดโปรแกรม...")
            self.running = False
        except Exception as e:
            self.add_alert_message(f"เกิดข้อผิดพลาด: {str(e)}", 'error')
            self.display_dashboard()
        finally:
            if 'process' in locals():
                process.terminate()

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
