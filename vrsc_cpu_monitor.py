import subprocess
import re
import time
from datetime import datetime
import json
import os
import threading
import sys


class VrscCpuMinerMonitor:
    def edit_config(self):
        """แก้ไขไฟล์ config.json"""
        config_path = os.path.expanduser('~/ccminer/config.json')
        
        try:
            subprocess.run(['nano', config_path])
            print("✅ แก้ไขไฟล์ config เรียบร้อยแล้ว")
            self.config = self.load_config()
        except Exception as e:
            print(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")

    def show_menu(self):
        """แสดงเมนูหลัก"""
        while True:
            print("\n" + "=========================")
            print("VRSC CPU Miner run|edit ║")
            print("=========================")
            print("1. เริ่มการขุด (run)")
            print("2. แก้ไข config (edit)")
            print("3. ออกจากโปรแกรม")
            
            choice = input("เลือกตัวเลือก: ").strip()
            
            if choice == "1":
                self.run()
            elif choice == "2":
                self.edit_config()
            elif choice == "3":
                print("ปิดโปรแกรม...")
                break
            else:
                print("⚠️ โปรดเลือกตัวเลือกที่ถูกต้อง")

    def __init__(self):
        self.hashrate_history = []
        self.max_hashrate = 0  # เพิ่มตัวแปรเก็บค่าแรงขุดสูงสุด
        self.start_time = time.time()
        self.max_history = 30
        self.config = self.load_config()
        self.last_difficulty = None
        self.last_update_time = None
        self.last_lines = []
        self.max_last_lines = 2
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
            'block': 0
        }

    def clean_log_line(self, line):
        """ตรวจสอบและคัดกรองข้อความแจ้งเตือนจาก CC Miner"""
        red_alert = re.search(r'\x1b\[31m(.*?)\x1b\[0m', line)
        if red_alert:
            return ('red', red_alert.group(1).strip())

        yellow_alert = re.search(r'\x1b\[33m(.*?)\x1b\[0m', line)
        if yellow_alert:
            return ('yellow', yellow_alert.group(1).strip())

        important_messages = [
            'error', 'fail', 'warning', 'disconnect',
            'reject', 'timeout', 'disconnected', 'connection lost',
            'stratum error', 'invalid share', 'high temperature',
            'retry', 'failed', 'disconnected from', 'network error'
        ]

        line_lower = line.lower()
        if any(msg in line_lower for msg in important_messages):
            clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            clean_line = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', clean_line)
            clean_line = re.sub(r'\(\d{2}:\d{2}:\d{2}\)', '', clean_line)
            return ('yellow', clean_line.strip())

        return None

    def add_alert_message(self, color, message):
        """เพิ่มข้อความแจ้งเตือนพร้อมระบุสี"""
        if not message or len(message) > 200:
            return

        timestamp = datetime.now().strftime('%H:%M:%S')
        self.alert_messages.append({
            'color': color,
            'message': f"[{timestamp}] {message}",
            'time': time.time()
        })
        if len(self.alert_messages) > 5:
            self.alert_messages.pop(0)

    def load_config(self):
        default_config = {
            'wallet_address': 'ไม่ระบุ',
            'miner_name': 'ไม่ระบุ',
            'user': 'ไม่ระบุ',
            'pass': 'ไม่ระบุ',
            'algo': 'ไม่ระบุ',
            'threads': 'ไม่ระบุ',
            'pools': ['ไม่ระบุ'],
            'cpu-priority': 'ไม่ระบุ',
            'cpu-affinity': 'ไม่ระบุ',
            'retry-pause': 'ไม่ระบุ',
            'api-allow': 'ไม่ระบุ',
            'api-bind': 'ไม่ระบุ',
            'base_wallet': 'ไม่ระบุ'
        }

        try:
            config_paths = [
                'config.json',
                '/data/data/com.termux/files/home/config.json',
                '/data/data/com.termux/files/usr/etc/verus/config.json'
            ]

            for path in config_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        loaded_config = json.load(f)

                        wallet = loaded_config.get('wallet_address',
                                                   loaded_config.get('user', 'ไม่ระบุ'))
                        if '.' in wallet:
                            base_wallet, miner_name = wallet.rsplit('.', 1)
                            loaded_config['base_wallet'] = base_wallet
                            loaded_config['miner_name'] = miner_name
                        else:
                            loaded_config['base_wallet'] = wallet

                        if ('pools' in loaded_config and
                                isinstance(loaded_config['pools'], list) and
                                len(loaded_config['pools']) > 0):
                            first_pool = loaded_config['pools'][0]
                            if isinstance(first_pool, dict):
                                pool_str = (f"{first_pool.get('name', 'ไม่มีชื่อ')} "
                                            f"({first_pool.get('url', 'ไม่มีURL')})")
                                loaded_config['pools'] = [pool_str]
                            else:
                                loaded_config['pools'] = [str(first_pool)]

                        default_config.update(loaded_config)
                    break
        except Exception as e:
            self.add_alert_message('red', f"ไม่สามารถโหลด config ได้: {str(e)}")

        return default_config

    def parse_miner_output(self, line):
        updated = False

        # ตรวจสอบและเพิ่มข้อความแจ้งเตือน
        alert = self.clean_log_line(line)
        if alert:
            color, message = alert
            self.add_alert_message(color, message)
            updated = True

        patterns = {
            'hashrate': [
                re.compile(r'(\d+\.?\d*)\s*(H|kH|MH|GH)/s'),
                re.compile(r'hashrate:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE),
                re.compile(r'speed:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE)
            ],
            'accepted_rejected': [
                re.compile(r'accepted\s*:\s*(\d+)\s*/\s*(\d+)', re.IGNORECASE),
                re.compile(r'accepted\s*=\s*(\d+)\s*rejected\s*=\s*(\d+)', re.IGNORECASE),
                re.compile(r'yes!:\s*(\d+)\s*no!:\s*(\d+)', re.IGNORECASE)
            ],
            'difficulty': [
                re.compile(r'difficulty[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'diff[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'net diff[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'network difficulty[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'current difficulty[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'\[\d+\] diff[:\s]*(\d+\.?\d*)', re.IGNORECASE)
            ],
            'share': re.compile(r'share:\s*(\d+)/(\d+)', re.IGNORECASE),
            'block': re.compile(r'block:\s*(\d+)', re.IGNORECASE),
            'connection': [
                re.compile(r'connected to:\s*(.*)', re.IGNORECASE),
                re.compile(r'pool:\s*(.*)', re.IGNORECASE),
                re.compile(r'stratum:\s*(.*)', re.IGNORECASE),
                re.compile(r'connecting to:\s*(.*)', re.IGNORECASE)
            ]
        }

        # หาค่า difficulty
        for pattern in patterns['difficulty']:
            match = pattern.search(line)
            if match:
                try:
                    new_diff = float(match.group(1))
                    if new_diff != self.miner_data['difficulty']:
                        self.miner_data['difficulty'] = new_diff
                        updated = True
                    self.last_difficulty = new_diff
                    self.last_update_time = time.time()
                    break
                except (ValueError, IndexError):
                    continue

        # หาค่า accepted และ rejected
        for pattern in patterns['accepted_rejected']:
            match = pattern.search(line)
            if match:
                try:
                    if pattern.pattern == r'accepted\s*:\s*(\d+)\s*/\s*(\d+)':
                        accepted = int(match.group(1))
                        total = int(match.group(2))
                        rejected = total - accepted
                    else:
                        accepted = int(match.group(1))
                        rejected = int(match.group(2))

                    if accepted != self.miner_data['accepted'] or rejected != self.miner_data['rejected']:
                        self.miner_data['accepted'] = accepted
                        self.miner_data['rejected'] = rejected
                        updated = True
                    break
                except (ValueError, IndexError) as e:
                    continue

        # หาค่า hashrate และ block
        for key in ['hashrate', 'block']:
            if key in patterns:
                if isinstance(patterns[key], list):
                    for pattern in patterns[key]:
                        match = pattern.search(line)
                        if match:
                            try:
                                if key == 'hashrate':
                                    value = float(match.group(1))
                                    unit = match.group(2).upper()
                                    conversions = {
                                        'H': 1,
                                        'KH': 1000,
                                        'MH': 1000000,
                                        'GH': 1000000000
                                    }
                                    value *= conversions.get(unit, 1)
                                    
                                    # อัพเดทค่าแรงขุดสูงสุด
                                    if value > self.max_hashrate:
                                        self.max_hashrate = value
                                        self.add_alert_message('green', f"แรงขุดสูงสุดใหม่: {self.format_hashrate(value)}")
                                    
                                    if value != self.miner_data['hashrate']:
                                        self.miner_data['hashrate'] = value
                                        updated = True
                                    self.hashrate_history.append(value)
                                    if len(self.hashrate_history) > self.max_history:
                                        self.hashrate_history.pop(0)
                                else:
                                    new_value = int(match.group(1))
                                    if new_value != self.miner_data[key]:
                                        self.miner_data[key] = new_value
                                        updated = True
                                break
                            except:
                                continue

        # หาค่าสถานะการเชื่อมต่อ
        if 'connection' in patterns:
            for pattern in patterns['connection']:
                match = pattern.search(line)
                if match:
                    try:
                        if 'connected' in line.lower():
                            new_status = "✅ เชื่อมต่อแล้ว"
                            if self.miner_data['connection']['status'] != new_status:
                                self.add_alert_message('green', "เชื่อมต่อพูลแล้ว")
                        elif 'connecting' in line.lower():
                            new_status = "🔄 กำลังเชื่อมต่อ"
                            if self.miner_data['connection']['status'] != new_status:
                                self.add_alert_message('yellow', "กำลังเชื่อมต่อพูล...")
                        else:
                            new_status = self.miner_data['connection']['status']

                        if new_status != self.miner_data['connection']['status']:
                            self.miner_data['connection']['status'] = new_status
                            updated = True
                        break
                    except:
                        continue

        # ตรวจสอบการหยุดทำงานของ miner
        if "miner stopped" in line.lower() or "miner exited" in line.lower():
            self.add_alert_message('red', "เครื่องขุดหยุดทำงาน!")
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
        """แสดงผลข้อมูลการขุด"""
        COLORS = {
            'green': '\033[92m', 'yellow': '\033[93m',
            'red': '\033[91m', 'blue': '\033[94m',
            'cyan': '\033[96m', 'purple': '\033[95m',
            'reset': '\033[0m', 'bold': '\033[1m',
            'brown': '\033[33m',
            'Light_Gray': '\033[37m',
            'yellow_bg': '\033[43m',
            'green_bg': '\033[42m',
            'orange_bg': '\033[48;5;208m',
            'black_text': '\033[30m',
            'white_bg': '\033[48;5;15m',
            'orange_text': '\033[38;5;208m',
            'purple_bg': '\033[48;5;54m'
        }

        # ล้างหน้าจอ
        print("\033[2J\033[H", end="")

        # ส่วนหัว
        print(f"{COLORS['bold']}{COLORS['purple']} 🚀🚀 VRSC Miner Edit by..OK_error 🚀🚀{COLORS['reset']}")
        print(f"{COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")
        # ส่วนสถานะการเชื่อมต่อ
        #print(f"{COLORS['brown']}สถานะการเชื่อมต่อพูล :{COLORS['reset']} {self.miner_data['connection']['status']}")
        # ส่วนแสดง Config
        print(
            f"{COLORS['brown']}Wallet{COLORS['reset']} : {COLORS['orange_text']}{self.config.get('base_wallet', 'ไม่ระบุ')}{COLORS['reset']}")
        print(
            f"{COLORS['brown']}Miner{COLORS['reset']}     : {COLORS['orange_text']}{self.config.get('miner_name', 'ไม่ระบุ')}{COLORS['reset']}")
        print(
            f"{COLORS['brown']}Threads{COLORS['reset']}   : {COLORS['orange_text']}{self.config.get('threads', 'ไม่ระบุ')}{COLORS['reset']}")
        print(
            f"{COLORS['brown']}Algorithm{COLORS['reset']} : {COLORS['orange_text']}{self.config.get('algo', 'ไม่ระบุ')}{COLORS['reset']}")
        print(
            f"{COLORS['brown']}Password{COLORS['reset']}  : {COLORS['orange_text']}{self.config.get('pass', 'ไม่ระบุ')}{COLORS['reset']}")

        # ส่วนแสดงแจ้งเตือน
        current_time = time.time()
        recent_alerts = [alert for alert in self.alert_messages
                         if current_time - alert['time'] < 300]  # แสดงแจ้งเตือนภายใน 5 นาที

        if recent_alerts:
            print(f"  📢 {COLORS['white_bg']}{COLORS['purple']}Alarm{COLORS['reset']} ⚠️")
            for alert in recent_alerts[-2:]:  # แสดง 2 ข้อความล่าสุด
                color_code = COLORS[alert['color']]
                print(f"{color_code}{alert['message']}{COLORS['reset']}")
            print()

        # ส่วนสถานะการขุด
        print(f"{COLORS['green']}《《《{COLORS['reset']}{COLORS['bold']}{COLORS['purple']} Working {COLORS['reset']}{COLORS['green']}》》》{COLORS['reset']}")
        print(f"  {COLORS['white_bg']}{COLORS['black_text']}Miner{COLORS['reset']} : {COLORS['green_bg']}{self.config.get('miner_name', 'ไม่ระบุ')}{COLORS['reset']}")
        
        # แสดง hashrate ปัจจุบัน
        hashrate = self.miner_data['hashrate']
        if hashrate > 10000:
            color = 'green'
        elif hashrate > 1000:
            color = 'yellow'
        else:
            color = 'red'
        print(f"  {COLORS['green_bg']}{COLORS['black_text']}Hashrate{COLORS['reset']} : "
              f"{COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']} ⚡ ⚡")

        # แสดง hashrate สูงสุด (Max Hashrate)
        max_hr_color = 'purple'  # สีสำหรับแสดงค่าแรงขุดสูงสุด
        print(f"  {COLORS['purple_bg']}{COLORS['green']}Max Hashrate{COLORS['reset']} : "
              f"{COLORS[max_hr_color]}{self.format_hashrate(self.max_hashrate)}{COLORS['reset']} 🏆")

        # แสดง difficulty
        difficulty = self.miner_data['difficulty']
        if difficulty > 1000000:
            diff_color = 'red'
            diff_str = f"{difficulty / 1000000:.2f} M"
        elif difficulty > 1000:
            diff_color = 'yellow'
            diff_str = f"{difficulty / 1000:.2f} K"
        else:
            diff_color = 'green'
            diff_str = f"{difficulty:.2f}"
        print(f"  {COLORS['yellow_bg']}{COLORS['black_text']}Difficulty{COLORS['reset']} : "
              f"{COLORS[diff_color]}{diff_str}{COLORS['reset']}")

        # แสดง shares
        accepted = self.miner_data['accepted']
        rejected = self.miner_data['rejected']
        total = accepted + rejected
        ratio = (accepted / total * 100) if total > 0 else 100

        ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
        print(f"  {COLORS['orange_bg']}{COLORS['black_text']}Shares{COLORS['reset']} : "
              f"{COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
        print(f"    {COLORS['bold']}{COLORS['orange_text']}├─ {COLORS['reset']}{COLORS['green']}Accepted{COLORS['orange_text']} ┑ {COLORS['reset']}{COLORS['green']}{accepted}{COLORS['reset']}")
        print(f"    {COLORS['bold']}{COLORS['orange_text']}└─ {COLORS['reset']}{COLORS['red']}Rejected{COLORS['orange_text']} ┙ {COLORS['reset']}{COLORS['red']}{rejected}{COLORS['reset']}")
        

    def run(self):
        try:
            process = subprocess.Popen(
                ["./start.sh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            print("กำลังเริ่มต้นเครื่องขุด...กด Ctrl+C เพื่อหยุด")
            self.display_dashboard()

            for line in iter(process.stdout.readline, ''):
                if self.parse_miner_output(line):
                    self.display_dashboard()

        except KeyboardInterrupt:
            print("\nกำลังหยุดการขุด...")
            self.running = False
        except Exception as e:
            self.add_alert_message('red', f"เกิดข้อผิดพลาด: {str(e)}")
            print(f"\nเกิดข้อผิดพลาด: {e}")
            self.running = False
        finally:
            if 'process' in locals():
                process.terminate()
                process.wait()


if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
    if len(sys.argv) > 1:
        if sys.argv[1] == "run":
            monitor.run()
        elif sys.argv[1] == "edit":
            monitor.edit_config()
        else:
            print("คำสั่งไม่ถูกต้อง [run|edit]")
    else:
        monitor.show_menu()
