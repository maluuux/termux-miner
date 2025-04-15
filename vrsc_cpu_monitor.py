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
            print(f"ไม่สามารถโหลด config ได้: {e}")

        return default_config

    def parse_miner_output(self, line):
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

        updated = False

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
                        new_status = match.group(1).strip()
                        if 'connected' in line.lower():
                            self.miner_data['connection']['status'] = f"เชื่อมต่อแล้ว: {new_status}"
                            # พยายามแยก URL จากข้อมูลการเชื่อมต่อ
                            if '://' in new_status:
                                self.miner_data['connection']['url'] = new_status.split('://')[1].split('/')[0]
                            updated = True
                        elif 'connecting' in line.lower():
                            self.miner_data['connection']['status'] = f"กำลังเชื่อมต่อ: {new_status}"
                            updated = True
                        break
                    except:
                        continue

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
            'orange_text': '\033[38;5;208m'
        }

        # ล้างหน้าจอ
        print("\033[2J\033[H", end="")

        # ส่วนหัว
        print(f"{COLORS['bold']}{COLORS['purple']}VRSC Miner Edit by ...... {COLORS['reset']}")
        print(f"   {COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")

        # ส่วนข้อมูลผู้ใช้และ Miner
        print(f"{COLORS['bold']}{COLORS['purple']}Show settings.......{COLORS['reset']}")
        print(f"  {COLORS['brown']}Wallet{COLORS['reset']} : "
              f"{COLORS['orange_text']}{self.config.get('base_wallet', 'ไม่ระบุ')}{COLORS['reset']}")
        print(f"  {COLORS['brown']}Miner{COLORS['reset']} : "
              f"{COLORS['orange_text']}{self.config.get('miner_name', 'ไม่ระบุ')}{COLORS['reset']}")
        print(f"  {COLORS['brown']}Threads{COLORS['reset']} : "
              f"{COLORS['orange_text']}{self.config.get('threads', 'ไม่ระบุ')}{COLORS['reset']}")
        print(f"  {COLORS['brown']}Algorithm{COLORS['reset']} : "
              f"{COLORS['orange_text']}{self.config.get('algo', 'ไม่ระบุ')}{COLORS['reset']}")
        print(f"  {COLORS['brown']}Password{COLORS['reset']} : "
              f"{COLORS['orange_text']}{self.config.get('pass', 'ไม่ระบุ')}{COLORS['reset']}")
        print("-" * 40)

        # ส่วนสถานะการขุด
        print(f"{COLORS['bold']}{COLORS['purple']}=== ⚡ Status Miner ⚡ ==={COLORS['reset']}")

        # ส่วนรันไทม์
        runtime = int(time.time() - self.start_time)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        seconds = runtime % 60
        print(f"{COLORS['cyan']} RunTime [ {COLORS['green']}{hours}:"
              f"{COLORS['yellow']}{minutes}:{COLORS['reset']}{seconds}{COLORS['reset']} ]")

        # แสดงสถานะการเชื่อมต่อ
        conn_status = self.miner_data['connection']
        print(f"\n  {COLORS['bold']}{COLORS['blue']}=== สถานะการเชื่อมต่อ ==={COLORS['reset']}")
        print(f"  {COLORS['brown']}พูล:{COLORS['reset']} {COLORS['green']}{conn_status['pool']}{COLORS['reset']}")
        print(f"  {COLORS['brown']}URL:{COLORS['reset']} {COLORS['cyan']}{conn_status['url']}{COLORS['reset']}")
        
        # กำหนดสีสถานะตามสถานะการเชื่อมต่อ
        if 'เชื่อมต่อแล้ว' in conn_status['status']:
            status_color = COLORS['green']
        elif 'กำลังเชื่อมต่อ' in conn_status['status']:
            status_color = COLORS['yellow']
        else:
            status_color = COLORS['red']
        
        print(f"  {COLORS['brown']}สถานะ:{COLORS['reset']} {status_color}{conn_status['status']}{COLORS['reset']}")

        # แสดง hashrate
        hashrate = self.miner_data['hashrate']
        if hashrate > 10000:
            color = 'green'
        elif hashrate > 1000:
            color = 'yellow'
        else:
            color = 'red'
        print(f"\n  {COLORS['green_bg']}{COLORS['black_text']}Hashrate{COLORS['reset']} : "
              f"{COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']} 🚀 🚀")

        # แสดง difficulty
        current_diff = self.miner_data['difficulty']
        diff_color = 'green' if current_diff < 100000 else 'brown' if current_diff < 300000 else 'yellow'
        print(f"  {COLORS['yellow_bg']}{COLORS['black_text']}Difficulty {COLORS['reset']}: "
              f"{COLORS[diff_color]}{current_diff:.2f}{COLORS['reset']}")

        # แสดง shares
        accepted = self.miner_data['accepted']
        rejected = self.miner_data['rejected']
        total = accepted + rejected
        ratio = (accepted / total * 100) if total > 0 else 100

        ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
        print(f"\n  {COLORS['orange_bg']}{COLORS['black_text']}Shares {COLORS['reset']} = "
              f"{COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
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

            # แสดง dashboard เริ่มต้น
            self.display_dashboard()

            for line in iter(process.stdout.readline, ''):
                if self.parse_miner_output(line):  # ถ้ามีการอัปเดตข้อมูล
                    self.display_dashboard()  # แสดงผลข้อมูลใหม่

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
