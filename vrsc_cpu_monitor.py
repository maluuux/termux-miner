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
                        
                        # แยก wallet address จาก user ถ้าไม่ระบุ wallet_address โดยตรง
                        if 'wallet_address' not in loaded_config and 'user' in loaded_config:
                            user_parts = loaded_config['user'].split('.')
                            if len(user_parts) > 0:
                                loaded_config['wallet_address'] = user_parts[0]
                            
                            if len(user_parts) > 1:
                                loaded_config['miner_name'] = user_parts[1]
                        
                        # ปรับโครงสร้าง pools
                        if 'pools' in loaded_config and isinstance(loaded_config['pools'], list):
                            if len(loaded_config['pools']) > 0 and isinstance(loaded_config['pools'][0], dict):
                                loaded_config['pools'] = [pool['url'] for pool in loaded_config['pools'] if 'url' in pool]
                        
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
            'accepted': [
                re.compile(r'accepted:\s*(\d+)', re.IGNORECASE),
                re.compile(r'yes!:\s*(\d+)', re.IGNORECASE)
            ],
            'rejected': [
                re.compile(r'rejected:\s*(\d+)', re.IGNORECASE),
                re.compile(r'no!:\s*(\d+)', re.IGNORECASE)
            ],
            'difficulty': [
                re.compile(r'difficulty:\s*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'diff:\s*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'network difficulty:\s*(\d+\.?\d*)', re.IGNORECASE),
                re.compile(r'current difficulty:\s*(\d+\.?\d*)', re.IGNORECASE),
            ],
            'share': re.compile(r'share:\s*(\d+)/(\d+)', re.IGNORECASE),
            'block': re.compile(r'block:\s*(\d+)', re.IGNORECASE),
            'connection': re.compile(r'connected to:\s*(.*)', re.IGNORECASE)
        }
        
        results = {}
        
        # หา hashrate
        for pattern in patterns['hashrate']:
            match = pattern.search(line)
            if match:
                try:
                    value = float(match.group(1))
                    unit = match.group(2).upper()
                    conversions = {'H': 1, 'KH': 1000, 'MH': 1000000, 'GH': 1000000000}
                    value *= conversions.get(unit, 1)
                    results['hashrate'] = value
                    self.hashrate_history.append(value)
                    if len(self.hashrate_history) > self.max_history:
                        self.hashrate_history.pop(0)
                    break
                except:
                    continue
        
        # หา accepted/rejected
        for key, key_patterns in [('accepted', patterns['accepted']), ('rejected', patterns['rejected'])]:
            for pattern in key_patterns:
                match = pattern.search(line)
                if match:
                    try:
                        results[key] = int(match.group(1))
                        break
                    except:
                        continue
        
        # หาค่าอื่นๆ
        for key in ['difficulty', 'block', 'connection']:
            match = patterns[key].search(line)
            if match:
                try:
                    if key == 'difficulty':
                        results[key] = float(match.group(1))
                    else:
                        results[key] = match.group(1).strip()
                except:
                    pass
        
        # หา share (ถ้ามีรูปแบบ share: 10/15)
        match = patterns['share'].search(line)
        if match:
            try:
                results['accepted'] = int(match.group(1))
                results['rejected'] = int(match.group(2)) - int(match.group(1))
            except:
                pass
        
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
        COLORS = {
            'green': '\033[92m', 'yellow': '\033[93m',
            'red': '\033[91m', 'blue': '\033[94m',
            'cyan': '\033[96m', 'purple': '\033[95m',
            'reset': '\033[0m', 'bold': '\033[1m'
        }
        
        # ล้างหน้าจอ
        print("\033[2J\033[H", end="")
        
        # ส่วนหัว
        
        print(f"{COLORS['bold']}{COLORS['purple']}=== VRSC CPU Mining Dashboard ==={COLORS['reset']}")
        print("-" * 20)
        print(f"{COLORS['cyan']}⏱️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")
        print("-" * 20)
        
        # ส่วนข้อมูลผู้ใช้และ Miner
        print(f"{COLORS['bold']}👤 ข้อมูลผู้ขุด:{COLORS['reset']}")
        print(f"  ที่อยู่กระเป๋า: {COLORS['blue']}{self.config['wallet_address']}{COLORS['reset']}")
        print(f"  ชื่อ Miner: {COLORS['blue']}{self.config['miner_name']}{COLORS['reset']}")
        
        # ส่วนการตั้งค่าการขุด
        print(f"  Threads: {COLORS['blue']}{self.config['threads']}{COLORS['reset']}")
        print(f"  Pools:")
        for i, pool in enumerate(self.config['pools'], 1):
            print(f"    {i}. {COLORS['blue']}{pool}{COLORS['reset']}")
      
        print(" " * 30)
        
        # ส่วนสถานะการขุด
        print(f"{COLORS['bold']}📊 สถานะการขุด:{COLORS['reset']}")

         # ส่วนรันไทม์
        runtime = int(time.time() - self.start_time)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        seconds = runtime % 60
        print(f"{COLORS['bold']}⏳ เวลาการทำงาน: {hours}h {minutes}m {seconds}s{COLORS['reset']}")
        print(f"{COLORS['bold']}{COLORS['reset']}")
        
        if 'connection' in miner_data:
            print(f"  เชื่อมต่อกับ: {COLORS['green']}{miner_data['connection']}{COLORS['reset']}")
        
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            if hashrate > 10000:
                color = 'green'
            elif hashrate > 1000:
                color = 'yellow'
            else:
                color = 'red'
            
            
        
        if 'difficulty' in miner_data:
            print(f"  ความยาก: {miner_data['difficulty']:.2f}")
        
        if 'accepted' in miner_data or 'rejected' in miner_data:
            accepted = miner_data.get('accepted', 0)
            rejected = miner_data.get('rejected', 0)
            total = accepted + rejected
            ratio = (accepted / total * 100) if total > 0 else 100
            
            ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
            print(f"  Shares: {COLORS['green']}{accepted} ยอมรับ{COLORS['reset']} | "
                  f"{COLORS['red']}{rejected} ปฏิเสธ{COLORS['reset']} | "
                  f"{COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
            print(f"  แรงขุด: {COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']}")
            print("⛏️          ⛏️")
        if 'block' in miner_data:
            print(f"  บล็อกที่พบ: {COLORS['cyan']}{miner_data['block']}{COLORS['reset']}")
 
     
    
    def run(self):
        try:
            process = subprocess.Popen(
                ["./start.sh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print("กำลังเริ่มต้นเครื่องขุด... (กด Ctrl+C เพื่อหยุด)")
            
            for line in iter(process.stdout.readline, ''):
                miner_data = self.parse_miner_output(line)
                if miner_data:
                    self.display_dashboard(miner_data)
                
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
