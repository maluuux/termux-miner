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
        config = {
            'wallet': 'ไม่ระบุ',
            'miner_name': 'ไม่ระบุ',
            'threads': 'ไม่ระบุ',
            'pools': [],
            'algorithm': 'ไม่ระบุ'
        }
        
        try:
            # ลองหาไฟล์ config ในที่ต่างๆ
            config_paths = [
                'config.json',
                '/data/data/com.termux/files/home/config.json',
                '/data/data/com.termux/files/usr/etc/verus/config.json'
            ]
            
            for path in config_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        config.update(json.load(f))
                    break
                    
        except Exception as e:
            print(f"ไม่สามารถโหลด config ได้: {e}")
            
        return config
    
    def parse_miner_output(self, line):
        """Parse output จาก miner"""
        patterns = {
            'hashrate': [
                re.compile(r'(\d+\.?\d*)\s*(H|kH|MH|GH)/s'),
                re.compile(r'hashrate:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE),
                re.compile(r'speed:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE)
            ],
            'accepted': re.compile(r'accepted:\s*(\d+)', re.IGNORECASE),
            'rejected': re.compile(r'rejected:\s*(\d+)', re.IGNORECASE),
            'difficulty': re.compile(r'difficulty:\s*(\d+\.?\d*)', re.IGNORECASE),
            'share': re.compile(r'share:\s*(\d+)/(\d+)', re.IGNORECASE),
            'block': re.compile(r'block:\s*(\d+)', re.IGNORECASE)
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
        for key in ['accepted', 'rejected']:
            match = patterns[key].search(line)
            if match:
                try:
                    results[key] = int(match.group(1))
                except:
                    pass
        
        # หา difficulty
        match = patterns['difficulty'].search(line)
        if match:
            try:
                results['difficulty'] = float(match.group(1))
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
        
        # หา block
        match = patterns['block'].search(line)
        if match:
            try:
                results['block'] = int(match.group(1))
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
        print(f"{COLORS['cyan']}⏱️ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")
        print("-" * 60)
        
        # ส่วนการตั้งค่า
        print(f"{COLORS['bold']}⚙️ การตั้งค่า:{COLORS['reset']}")
        print(f"  กระเป๋า: {COLORS['blue']}{self.config['wallet']}{COLORS['reset']}")
        print(f"  ชื่อเครื่องขุด: {COLORS['blue']}{self.config['miner_name']}{COLORS['reset']}")
        print(f"  Threads: {COLORS['blue']}{self.config['threads']}{COLORS['reset']}")
        print(f"  Algorithm: {COLORS['blue']}{self.config['algorithm']}{COLORS['reset']}")
        print(f"  Pools:")
        for i, pool in enumerate(self.config['pools'], 1):
            print(f"    {i}. {COLORS['blue']}{pool}{COLORS['reset']}")
        
        print("-" * 60)
        
        # ส่วนสถานะการขุด
        print(f"{COLORS['bold']}📊 สถานะการขุด:{COLORS['reset']}")
        
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            if hashrate > 10000:
                color = 'green'
            elif hashrate > 1000:
                color = 'yellow'
            else:
                color = 'red'
            
            print(f"  แรงขุด: {COLORS[color]}{self.format_hashrate(hashrate)}{COLORS['reset']}")
        
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
        
        if 'block' in miner_data:
            print(f"  บล็อกที่พบ: {miner_data['block']}")
        
        print("-" * 60)
        
        # ส่วนรันไทม์
        runtime = int(time.time() - self.start_time)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        seconds = runtime % 60
        print(f"{COLORS['bold']}⏳ เวลาการทำงาน: {hours}h {minutes}m {seconds}s{COLORS['reset']}")
        print(f"{COLORS['bold']}{'='*60}{COLORS['reset']}")
    
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
