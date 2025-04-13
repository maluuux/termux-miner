import subprocess
import re
import time
from datetime import datetime
import json
import os
import sys
import logging

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30
        self.config = self.load_config()
        self.last_difficulty = None
        self.last_update_time = None
        self.log_file = os.path.expanduser("~/miner_log.txt")
        self.setup_logging()
        
        # สำหรับ Termux บน Android
        self.termux_mode = True if 'com.termux' in os.getcwd() else False
        self.clear_command = 'clear' if not self.termux_mode else 'clear'

    def setup_logging(self):
        """ตั้งค่าระบบบันทึก log"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('VRSC_Miner')

    def load_config(self):
        """โหลดการตั้งค่าจากไฟล์ config"""
        default_config = {
            'wallet_address': 'ไม่ระบุ',
            'miner_name': 'ไม่ระบุ',
            'user': 'ไม่ระบุ',
            'pass': 'x',
            'algo': 'verushash',
            'threads': '2',
            'pools': ['na.luckpool.net:3956'],
            'cpu-priority': '0',
            'retry-pause': '5'
        }

        try:
            config_paths = [
                os.path.expanduser('~/config.json'),
                '/data/data/com.termux/files/home/config.json',
                '/data/data/com.termux/files/usr/etc/verus/config.json'
            ]

            for path in config_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        loaded_config = json.load(f)
                        
                        # ปรับรูปแบบ wallet address สำหรับ Termux
                        if 'wallet_address' not in loaded_config and 'user' in loaded_config:
                            user_parts = loaded_config['user'].split('.')
                            loaded_config['wallet_address'] = user_parts[0]
                            if len(user_parts) > 1:
                                loaded_config['miner_name'] = user_parts[1]
                        
                        default_config.update(loaded_config)
                    break

        except Exception as e:
            self.logger.error(f"ไม่สามารถโหลด config ได้: {e}")

        return default_config

    def parse_miner_output(self, line):
        """Parse output จาก miner"""
        patterns = {
            'hashrate': [
                re.compile(r'(\d+\.?\d*)\s*(H|kH|MH|GH)/s'),
                re.compile(r'hashrate:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE),
                re.compile(r'speed:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE)
            ],
            'accepted': [
                re.compile(r'accepted:\s*(\d+)', re.IGNORECASE),
                re.compile(r'yes!:\s*(\d+)', re.IGNORECASE),
                re.compile(r'(\d+)/(\d+)')  # สำหรับรูปแบบ 1975/1990
            ],
            'rejected': [
                re.compile(r'rejected:\s*(\d+)', re.IGNORECASE),
                re.compile(r'no!:\s*(\d+)', re.IGNORECASE)
            ],
            'difficulty': [
                re.compile(r'difficulty[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'diff[:\s]*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'net diff[:\s]*(\d+\.?\d*)', re.IGNORECASE)
            ],
            'connection': re.compile(r'connected to:\s*(.*)', re.IGNORECASE),
            'connection_status': re.compile(r'status:\s*(\w+)', re.IGNORECASE)
        }

        results = {}

        # ตรวจสอบรูปแบบ X/Y ก่อน
        if 'accepted' in patterns:
            for pattern in patterns['accepted']:
                match = pattern.search(line)
                if match and len(match.groups()) >= 2:
                    try:
                        accepted = int(match.group(1))
                        total = int(match.group(2))
                        results['accepted'] = accepted
                        results['rejected'] = total - accepted
                        break
                    except (ValueError, IndexError):
                        continue

        # หาค่าอื่นๆ
        for key in patterns:
            if key not in results:  # ไม่เขียนทับค่าที่มีอยู่แล้ว
                if isinstance(patterns[key], list):
                    for pattern in patterns[key]:
                        match = pattern.search(line)
                        if match:
                            try:
                                if key == 'hashrate':
                                    value = float(match.group(1))
                                    unit = match.group(2).upper() if len(match.groups()) > 1 else 'H'
                                    conversions = {'H': 1, 'KH': 1000, 'MH': 1000000, 'GH': 1000000000}
                                    value *= conversions.get(unit, 1)
                                    results[key] = value
                                    self.hashrate_history.append(value)
                                    if len(self.hashrate_history) > self.max_history:
                                        self.hashrate_history.pop(0)
                                elif key == 'difficulty':
                                    diff_value = float(match.group(1))
                                    if diff_value > 1000000:
                                        diff_value = f"{diff_value/1000000:.2f}M"
                                    elif diff_value > 1000:
                                        diff_value = f"{diff_value/1000:.2f}K"
                                    results[key] = diff_value
                                    self.last_difficulty = diff_value
                                    self.last_update_time = time.time()
                                else:
                                    results[key] = int(match.group(1))
                                break
                            except (ValueError, IndexError):
                                continue
                else:
                    match = patterns[key].search(line)
                    if match:
                        results[key] = match.group(1).strip()

        return results

    def format_hashrate(self, hashrate):
        """จัดรูปแบบ hashrate"""
        if hashrate >= 1000000:
            return f"{hashrate/1000000:.2f} MH/s"
        elif hashrate >= 1000:
            return f"{hashrate/1000:.2f} kH/s"
        return f"{hashrate:.2f} H/s"

    def display_dashboard(self, miner_data):
        """แสดงผลข้อมูลการขุด"""
        # สีสำหรับ Termux (ใช้ ANSI colors)
        COLORS = {
            'green': '\033[92m', 'yellow': '\033[93m',
            'red': '\033[91m', 'blue': '\033[94m',
            'cyan': '\033[96m', 'purple': '\033[95m',
            'reset': '\033[0m', 'bold': '\033[1m',
            'white_bg': '\033[47m',
            'black_text': '\033[30m'
        }

        # ล้างหน้าจอ (ทำงานได้ทั้ง Termux และระบบอื่น)
        os.system(self.clear_command)

        # ส่วนหัว
        print(f"{COLORS['bold']}{COLORS['purple']}⚡ VRSC MINER FOR TERMUX ⚡{COLORS['reset']}")
        print(f"{COLORS['cyan']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")

        # ข้อมูลผู้ใช้
        print(f"\n{COLORS['bold']}👛 Wallet: {COLORS['green']}{self.config['wallet_address']}")
        print(f"⛏️ Miner: {COLORS['yellow']}{self.config.get('miner_name', 'ไม่ระบุ')}")
        print(f"🧵 Threads: {COLORS['cyan']}{self.config['threads']}{COLORS['reset']}")

        # สถานะการขุด
        print(f"\n{COLORS['bold']}=== MINING STATUS ===")
        
        # Runtime
        runtime = int(time.time() - self.start_time)
        hours, remainder = divmod(runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"⏱️ Runtime: {COLORS['green']}{hours}h {COLORS['yellow']}{minutes}m {COLORS['cyan']}{seconds}s{COLORS['reset']}")

        # Hashrate
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            color = 'green' if hashrate > 10000 else 'yellow' if hashrate > 1000 else 'red'
            print(f"🚀 Hashrate: {COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']}")

        # Difficulty
        if 'difficulty' in miner_data:
            print(f"📈 Difficulty: {COLORS['yellow']}{miner_data['difficulty']}{COLORS['reset']}")
        elif self.last_difficulty:
            print(f"📈 Difficulty: {COLORS['yellow']}{self.last_difficulty} (last){COLORS['reset']}")

        # Connection
        if 'connection' in miner_data:
            print(f"🌐 Pool: {COLORS['cyan']}{miner_data['connection']}{COLORS['reset']}")

        # Shares
        if 'accepted' in miner_data or 'rejected' in miner_data:
            accepted = miner_data.get('accepted', 0)
            rejected = miner_data.get('rejected', 0)
            total = accepted + rejected
            ratio = (accepted / total * 100) if total > 0 else 100
            
            ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
            
            # แสดงผลแบบปรับปรุงแล้ว
            print(f"\n{COLORS['bold']}📊 SHARES STATUS")
            print(f"✅ Accepted: {COLORS['green']}{accepted:,}{COLORS['reset']}")
            print(f"❌ Rejected: {COLORS['red']}{rejected:,}{COLORS['reset']}")
            print(f"📤 Total: {COLORS['cyan']}{total:,}{COLORS['reset']}")
            print(f"📈 Success Rate: {COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
            
            # Progress bar
            progress_width = 20
            filled = int(ratio * progress_width / 100)
            progress_bar = f"{COLORS['green']}{'█' * filled}{COLORS['reset']}{COLORS['red']}{'░' * (progress_width - filled)}{COLORS['reset']}"
            print(f"[{progress_bar}]")

    def run_miner_process(self):
        """รันกระบวนการขุด"""
        try:
            # สร้างคำสั่งสำหรับ Termux
            command = [
                "miner",  # เปลี่ยนเป็นชื่อ executable ของคุณ
                "--algo", self.config['algo'],
                "--server", self.config['pools'][0].split(':')[0],
                "--port", self.config['pools'][0].split(':')[1],
                "--user", f"{self.config['wallet_address']}.{self.config.get('miner_name', 'termux')}",
                "--pass", self.config['pass'],
                "--threads", str(self.config['threads']),
                "--cpu-priority", str(self.config['cpu-priority']),
                "--retry-pause", str(self.config['retry-pause'])
            ]
            
            # สำหรับ Termux บน Android
            if self.termux_mode:
                command.insert(0, "nice")  # ใช้ nice เพื่อลด priority
                command.insert(1, "-n") 
                command.insert(2, "19")

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            print(f"{'='*40}\nStarting VRSC Miner on Termux...\n{'='*40}")
            print(f"Press Ctrl+C to stop\n{'='*40}")

            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
                if output:
                    miner_data = self.parse_miner_output(output)
                    if miner_data:
                        self.display_dashboard(miner_data)
                        self.log_miner_data(miner_data)
                
                if error:
                    print(f"\033[91mERROR: {error.strip()}\033[0m")
                    self.logger.error(error.strip())

        except KeyboardInterrupt:
            print("\n🛑 Stopping miner...")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self.logger.error(f"Error: {str(e)}")
        finally:
            if 'process' in locals():
                process.terminate()
                process.wait()
            print("✅ Miner stopped")

    def log_miner_data(self, miner_data):
        """บันทึกข้อมูลการขุด"""
        log_message = (
            f"Hashrate: {self.format_hashrate(miner_data.get('hashrate', 0))} | "
            f"Accepted: {miner_data.get('accepted', 0)} | "
            f"Rejected: {miner_data.get('rejected', 0)} | "
            f"Diff: {miner_data.get('difficulty', 'N/A')}"
        )
        self.logger.info(log_message)

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run_miner_process()
