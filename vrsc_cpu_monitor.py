import subprocess
import re
import time
from datetime import datetime

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30  # จำนวนค่าที่เก็บไว้แสดงกราฟ
        
    def parse_miner_output(self, line):
        """Parse output for VRSC CPU mining"""
        patterns = {
            'rate': re.compile(r'(\d+\.\d+)\s*(H|kH|MH|GH)/s'),
            'accepted': re.compile(r'accepted:\s*(\d+)/'),
            'rejected': re.compile(r'rejected:\s*(\d+)'),
        }
        
        results = {}
        for key, pattern in patterns.items():
            match = pattern.search(line.lower())
            if match:
                if key == 'hashrate':
                    value = float(match.group(1))
                    unit = match.group(2)
                    # Convert to H/s
                    if unit == 'kH':
                        value *= 1000
                    elif unit == 'MH':
                        value *= 1000000
                    elif unit == 'GH':
                        value *= 1000000000
                    results[key] = value
                    # Keep history for chart
                    self.hashrate_history.append(value)
                    if len(self.hashrate_history) > self.max_history:
                        self.hashrate_history.pop(0)
                elif key in ['accepted', 'rejected']:
                    results[key] = int(match.group(1))
        
        return results
    
    def format_hashrate(self, hashrate):
        """Format hashrate to appropriate unit"""
        if hashrate >= 1000000:  # 1 MH/s
            return f"{hashrate/1000000:.2f} MH/s"
        elif hashrate >= 1000:   # 1 kH/s
            return f"{hashrate/1000:.2f} kH/s"
        return f"{hashrate:.2f} H/s"
    
    def display_hashrate_chart(self, current_hashrate):
        """Display a simple ASCII chart of hashrate history"""
        if not self.hashrate_history:
            return ""
        
        max_hash = max(self.hashrate_history)
        min_hash = min(self.hashrate_history)
        range_hash = max_hash - min_hash if max_hash != min_hash else 1
        
        chart_height = 5
        chart = []
        
        for i in range(chart_height, 0, -1):
            threshold = min_hash + (range_hash * i / chart_height)
            row = []
            for h in self.hashrate_history:
                row.append('▓' if h >= threshold else ' ')
            chart.append(''.join(row))
        
        # Add current hashrate indicator
        chart.append(f"Current: {self.format_hashrate(current_hashrate)}")
        chart.append(f"Min: {self.format_hashrate(min_hash)} | Max: {self.format_hashrate(max_hash)}")
        
        return '\n'.join(chart)
    
    def display_dashboard(self, miner_data):
        """Display the mining dashboard"""
        # ANSI Colors
        COLORS = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
        
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Header
        print(f"{COLORS['bold']}{COLORS['blue']}=== VRSC CPU Mining ==={COLORS['reset']}")
        print(f"{COLORS['cyan']}⛏️ แรงขุด VerusCoin (VRSC) - {datetime.now().strftime('%H:%M:%S')}{COLORS['reset']}")
        print("-" * 50)
        
        # Mining Status Section
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            if hashrate > 10000:
                hash_color = 'green'
            elif hashrate > 1000:
                hash_color = 'yellow'
            else:
                hash_color = 'red'
            
            print(f"{COLORS['bold']}แรงขุดปัจจุบัน:{COLORS['reset']}")
            print(f"{COLORS[hash_color]}{' ' * 10}{self.format_hashrate(hashrate)}{' ' * 10}{COLORS['reset']}")
            print("\n" + self.display_hashrate_chart(hashrate))
        
        if 'accepted' in miner_data or 'rejected' in miner_data:
            accepted = miner_data.get('accepted', 0)
            rejected = miner_data.get('rejected', 0)
            total = accepted + rejected
            ratio = (accepted / total * 100) if total > 0 else 100
            
            ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
            print(f"\n{COLORS['bold']}Shares:{COLORS['reset']} {COLORS['green']}{accepted} ยอมรับ{COLORS['reset']} | "
                  f"{COLORS['red']}{rejected} ปฏิเสธ{COLORS['reset']} | "
                  f"{COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
        
        print("-" * 50)
        runtime = int(time.time() - self.start_time)
        print(f"{COLORS['cyan']}Runtime: {runtime//3600}h {(runtime%3600)//60}m {runtime%60}s{COLORS['reset']}")
        print(f"{COLORS['bold']}{'='*50}{COLORS['reset']}")
    
    def run(self):
        # Start mining process
        process = subprocess.Popen(
            ["./start.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        try:
            for line in iter(process.stdout.readline, ''):
                miner_data = self.parse_miner_output(line)
                if miner_data:
                    self.display_dashboard(miner_data)
                    
        except KeyboardInterrupt:
            print("\nหยุดการตรวจสอบ...")
            process.terminate()
        finally:
            process.wait()

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
