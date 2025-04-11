import subprocess
import re
import time
from datetime import datetime

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30
        
    def parse_miner_output(self, line):
        """Parse output with more flexible patterns"""
        # Debug: แสดงบรรทัดที่ได้รับมา
        print(f"DEBUG RAW LINE: {line.strip()}")
        
        patterns = {
            'hashrate': [
                re.compile(r'(\d+\.?\d*)\s*(H|kH|MH|GH)/s'),  # รูปแบบมาตรฐาน
                re.compile(r'hashrate:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE),
                re.compile(r'speed:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE),
                re.compile(r'rate:\s*(\d+\.?\d*)\s*(H|kH|MH|GH)/s', re.IGNORECASE)
            ],
            'accepted': re.compile(r'accepted:\s*(\d+)', re.IGNORECASE),
            'rejected': re.compile(r'rejected:\s*(\d+)', re.IGNORECASE),
        }
        
        results = {}
        
        # ตรวจสอบ hashrate ทุกรูปแบบ
        for pattern in patterns['hashrate']:
            match = pattern.search(line)
            if match:
                try:
                    value = float(match.group(1))
                    unit = match.group(2).upper() if match.group(2) else 'H'
                    
                    # Convert to H/s
                    conversions = {'H': 1, 'KH': 1000, 'MH': 1000000, 'GH': 1000000000}
                    value *= conversions.get(unit, 1)
                    
                    results['hashrate'] = value
                    self.hashrate_history.append(value)
                    if len(self.hashrate_history) > self.max_history:
                        self.hashrate_history.pop(0)
                    break
                except (ValueError, IndexError) as e:
                    print(f"DEBUG Hashrate parse error: {e}")
                    continue
        
        # ตรวจสอบ accepted/rejected
        for key in ['accepted', 'rejected']:
            match = patterns[key].search(line)
            if match:
                try:
                    results[key] = int(match.group(1))
                except (ValueError, IndexError) as e:
                    print(f"DEBUG {key} parse error: {e}")
        
        return results
    
    def display_dashboard(self, miner_data):
        """Display simplified dashboard"""
        COLORS = {
            'green': '\033[92m', 'yellow': '\033[93m', 
            'red': '\033[91m', 'reset': '\033[0m',
            'bold': '\033[1m'
        }
        
        print("\033[2J\033[H", end="")  # Clear screen
        
        print(f"{COLORS['bold']}=== VRSC CPU Mining Monitor ==={COLORS['reset']}")
        print(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)
        
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            if hashrate >= 1000000:
                display = f"{hashrate/1000000:.2f} MH/s"
                color = 'green'
            elif hashrate >= 1000:
                display = f"{hashrate/1000:.2f} kH/s"
                color = 'yellow'
            else:
                display = f"{hashrate:.2f} H/s"
                color = 'red'
            
            print(f"{COLORS['bold']}Hashrate:{COLORS['reset']} {COLORS[color]}{display}{COLORS['reset']}")
        else:
            print(f"{COLORS['red']}No hashrate data found{COLORS['reset']}")
        
        print("-" * 40)
        
    def run(self):
        try:
            process = subprocess.Popen(
                ["/bin/bash", "./start.sh"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print("Starting miner... (Press Ctrl+C to stop)")
            
            for line in iter(process.stdout.readline, ''):
                miner_data = self.parse_miner_output(line)
                if miner_data:
                    self.display_dashboard(miner_data)
                
        except KeyboardInterrupt:
            print("\nStopping monitor...")
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            if 'process' in locals():
                process.terminate()
                process.wait()

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
