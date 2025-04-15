import subprocess
import re
import time
from datetime import datetime
import json
import os


class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30
        self.config = self.load_config()
        self.last_difficulty = None
        self.last_update_time = None
        self.miner_data = {}  # เพิ่มตัวแปรนี้เพื่อเก็บข้อมูล

    def load_config(self):
        """โหลดการตั้งค่าจากไฟล์ config"""
        default_config = {
            'wallet_address': 'ไม่ระบุ',
            'miner_name': 'ไม่ระบุ',
            'user': 'ไม่ระบุ',
            'pass': 'ไม่ระบุ',
            'algo': 'ไม่ระบุ',
            'threads': 'ไม่ระบุ',
            'pools': [],
            'cpu-priority': 'ไม่ระบุ',
            'cpu-affinity': 'ไม่ระบุ',
            'retry-pause': 'ไม่ระบุ',
            'api-allow': 'ไม่ระบุ',
            'api-bind': 'ไม่ระบุ'
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
                        default_config.update(loaded_config)
                    break
        except Exception as e:
            print(f"ไม่สามารถโหลด config ได้: {e}")

        return default_config

    def parse_miner_output(self, line):
        """Parse output จาก miner"""
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
            'connection': re.compile(r'connected to:\s*(.*)', re.IGNORECASE)
        }

        results = {}

        # หาค่า difficulty
        for pattern in patterns['difficulty']:
            match = pattern.search(line)
            if match:
                try:
                    results['difficulty'] = float(match.group(1))
                    self.last_difficulty = results['difficulty']
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
                        results['accepted'] = accepted
                        results['rejected'] = total - accepted
                    else:
                        results['accepted'] = int(match.group(1))
                        results['rejected'] = int(match.group(2))
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG: Error parsing accepted/rejected - {e}")

        # หาค่าอื่นๆ
        for key in ['hashrate', 'block', 'connection']:
            if key in patterns:
                if isinstance(patterns[key], list):
                    for pattern in patterns[key]:
                        match = pattern.search(line)
                        if match:
                            try:
                                if key == 'hashrate':
                                    value = float(match.group(1))
                                    unit = match.group(2).upper()
                                    conversions = {'H': 1, 'KH': 1000, 'MH': 1000000, 'GH': 1000000000}
                                    value *= conversions.get(unit, 1)
                                    results[key] = value
                                    self.hashrate_history.append(value)
                                    if len(self.hashrate_history) > self.max_history:
                                        self.hashrate_history.pop(0)
                                else:
                                    results[key] = int(match.group(1))
                                break
                            except:
                                continue
                else:
                    match = patterns[key].search(line)
                    if match:
                        try:
                            results[key] = match.group(1).strip()
                        except:
                            pass

        self.miner_data = results  # อัปเดตข้อมูลล่าสุด
        return results

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
            'orange_text': '\033[38;5;208m'
        }

        # ล้างหน้าจอ
        print("\033[2J\033[H", end="")

        # ส่วนหัว
        print(f"{COLORS['bold']}{COLORS['purple']}VRSC Miner Edit by ...... {COLORS['reset']}")
        print(f"   {COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")

        # ส่วนข้อมูลผู้ใช้และ Miner
        print(f"{COLORS['bold']}{COLORS['purple']}Show settings.......{COLORS['reset']}")
        print(
            f"  {COLORS['brown']}Wallet{COLORS['reset']} : {COLORS['orange_text']}{self.config['wallet_address']}{COLORS['reset']}")
        print(
            f"  {COLORS['brown']}Miner{COLORS['reset']} : {COLORS['orange_text']}{self.config['miner_name']}{COLORS['reset']}")
        print(
            f"  {COLORS['brown']}Threads{COLORS['reset']} : {COLORS['orange_text']}{self.config['threads']}{COLORS['reset']}")
        print(
            f"  {COLORS['brown']}Pass{COLORS['reset']} : {COLORS['orange_text']}{self.config['pass']}{COLORS['reset']}")
        print(
            f"  {COLORS['brown']}Pools{COLORS['reset']} : {COLORS['orange_text']}{', '.join([f'{i}.{pool}' for i, pool in enumerate(self.config['pools'], 1)])}{COLORS['reset']}")

        print("-" * 0)

        # ส่วนสถานะการขุด
        print(f"{COLORS['bold']}{COLORS['purple']}=== ⚡ Status Miner ⚡ ==={COLORS['reset']}")

        # ส่วนรันไทม์
        runtime = int(time.time() - self.start_time)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        seconds = runtime % 60
        print(
            f"{COLORS['cyan']} RunTime [ {COLORS['green']}{hours}:{COLORS['yellow']}{minutes}:{COLORS['reset']}{seconds}{COLORS['reset']} ]")
        print(f"{COLORS['bold']}{COLORS['reset']}")

        # ใช้ self.miner_data แทน miner_data
        if 'connection' in self.miner_data:
            print(f"  เชื่อมต่อกับ: {COLORS['green']}{self.miner_data['connection']}{COLORS['reset']}")

        if 'hashrate' in self.miner_data:
            hashrate = self.miner_data['hashrate']
            if hashrate > 10000:
                color = 'green'
            elif hashrate > 1000:
                color = 'yellow'
            else:
                color = 'red'
            print(
                f"  {COLORS['green_bg']}{COLORS['black_text']}Hashrate{COLORS['reset']} : {COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']} 🚀 🚀")

        # แสดง difficulty
        current_diff = self.miner_data.get('difficulty')
        if current_diff is not None:
            diff_color = 'green' if current_diff < 100000 else 'brown' if current_diff < 300000 else 'yellow'
            print(
                f"  {COLORS['yellow_bg']}{COLORS['black_text']}Difficulty {COLORS['reset']}: {COLORS[diff_color]}{current_diff:.2f}{COLORS['reset']}")
        else:
            print(
                f"  {COLORS['yellow_bg']}{COLORS['black_text']}    กำลังค้นหา... {COLORS['reset']}")

        # แสดง shares
        if 'accepted' in self.miner_data or 'rejected' in self.miner_data:
            accepted = self.miner_data.get('accepted', 0)
            rejected = self.miner_data.get('rejected', 0)
            total = accepted + rejected
            ratio = (accepted / total * 100) if total > 0 else 100

            ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
            print(
                f"  {COLORS['orange_bg']}{COLORS['black_text']}Shares {COLORS['reset']} = {COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
            print(f"  {COLORS['green']}Accepted!! {accepted} {COLORS['reset']}")
            print(f"  {COLORS['red']}Rejected!! {rejected} {COLORS['reset']}")

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

            for line in iter(process.stdout.readline, ''):
                self.parse_miner_output(line)  # อัปเดต self.miner_data
                self.display_dashboard()  # แสดงผลข้อมูล

        except KeyboardInterrupt:
            print("\nกำลังหยุดการตรวจสอบ...")
        except Exception as e:
            print(f"\nเกิดข้อผิดพลาด: {e}")
        finally:
            if 'process' in locals():
                process.terminate()
                process.wait()


if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
