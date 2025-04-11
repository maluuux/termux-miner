import subprocess
import re
import time
import psutil
from datetime import datetime

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30  # จำนวนค่าที่เก็บไว้แสดงกราฟ
        
    def parse_miner_output(self, line):
        """Parse output for VRSC CPU mining"""
        patterns = {
            'hashrate': re.compile(r'(\d+\.\d+)\s*(H|kH|MH|GH)/s'),
            'accepted': re.compile(r'accepted:\s*(\d+)/'),
            'rejected': re.compile(r'rejected:\s*(\d+)'),
            'shares': re.compile(r'shares:\s*(\d+)\/(\d+)'),
            'difficulty': re.compile(r'difficulty\s*(\d+\.\d+)'),
            'block': re.compile(r'block:\s*(\d+)'),
            'uptime': re.compile(r'uptime:\s*(\d+d)?\s*(\d+h)?\s*(\d+m)?')
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
                elif key == 'shares':
                    results['accepted'] = int(match.group(1))
                    results['rejected'] = int(match.group(2))
                elif key in ['accepted', 'rejected', 'block']:
                    results[key] = int(match.group(1))
                elif key == 'difficulty':
                    results[key] = float(match.group(1))
                elif key == 'uptime':
                    days = int(match.group(1)[:-1]) if match.group(1) else 0
                    hours = int(match.group(2)[:-1]) if match.group(2) else 0
                    minutes = int(match.group(3)[:-1]) if match.group(3) else 0
                    results['uptime'] = f"{days}d {hours}h {minutes}m"
        
        return results
    
    def get_system_stats(self):
        """Get CPU and system statistics"""
        stats = {}
        try:
            # CPU Temperature (may not work on all devices)
            try:
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    stats['cpu_temp'] = float(f.read()) / 1000
            except:
                pass
            
            # CPU Usage
            stats['cpu_usage'] = psutil.cpu_percent(interval=1)
            stats['cpu_cores'] = psutil.cpu_count(logical=False)
            
            # Memory Usage
            mem = psutil.virtual_memory()
            stats['mem_used'] = mem.used / (1024**2)  # MB
            stats['mem_total'] = mem.total / (1024**2)  # MB
            
            # Battery (if available)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    stats['battery_percent'] = battery.percent
                    stats['battery_charging'] = battery.power_plugged
            except:
                pass
            
        except Exception as e:
            print(f"Error getting system stats: {e}")
        
        return stats
    
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
    
    def display_dashboard(self, miner_data, system_stats):
        """Display the mining dashboard"""
        # ANSI Colors
        COLORS = {
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'purple': '\033[95m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
        
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Header
        print(f"{COLORS['bold']}{COLORS['purple']}=== VRSC CPU Mining Dashboard ==={COLORS['reset']}")
        print(f"{COLORS['blue']}⛏️ Mobile CPU Miner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['reset']}")
        print("-" * 60)
        
        # Mining Status Section
        print(f"{COLORS['bold']}🔧 สถานะการขุด:{COLORS['reset']}")
        
        if 'hashrate' in miner_data:
            hashrate = miner_data['hashrate']
            if hashrate > 10000:
                hash_color = 'green'
            elif hashrate > 1000:
                hash_color = 'yellow'
            else:
                hash_color = 'red'
            
            print(f"  แรงขุด: {COLORS[hash_color]}{self.format_hashrate(hashrate)}{COLORS['reset']}")
            print(self.display_hashrate_chart(hashrate))
        
        if 'accepted' in miner_data or 'rejected' in miner_data:
            accepted = miner_data.get('accepted', 0)
            rejected = miner_data.get('rejected', 0)
            total = accepted + rejected
            ratio = (accepted / total * 100) if total > 0 else 100
            
            ratio_color = 'green' if ratio > 95 else 'yellow' if ratio > 80 else 'red'
            print(f"  Shares: {COLORS['green']}{accepted} ยอมรับ{COLORS['reset']} | "
                  f"{COLORS['red']}{rejected} ปฏิเสธ{COLORS['reset']} | "
                  f"{COLORS[ratio_color]}{ratio:.1f}%{COLORS['reset']}")
        
        if 'difficulty' in miner_data:
            print(f"  ความยาก: {miner_data['difficulty']:.2f}")
        
        if 'block' in miner_data:
            print(f"  พบบล็อก: {miner_data['block']}")
        
        if 'uptime' in miner_data:
            print(f"  ระยะเวลาขุด: {miner_data['uptime']}")
        
        # System Status Section
        print(f"\n{COLORS['bold']}🖥️ สถานะระบบ:{COLORS['reset']}")
        
        if 'cpu_temp' in system_stats:
            temp = system_stats['cpu_temp']
            temp_color = 'green' if temp < 60 else 'yellow' if temp < 70 else 'red'
            print(f"  อุณหภูมิ CPU: {COLORS[temp_color]}{temp:.1f}°C{COLORS['reset']}")
        
        if 'cpu_usage' in system_stats:
            usage = system_stats['cpu_usage']
            usage_color = 'green' if usage < 70 else 'yellow' if usage < 90 else 'red'
            print(f"  การใช้ CPU: {COLORS[usage_color]}{usage:.1f}%{COLORS['reset']}")
        
        if 'cpu_cores' in system_stats:
            print(f"  จำนวน Cores: {system_stats['cpu_cores']}")
        
        if 'mem_used' in system_stats and 'mem_total' in system_stats:
            mem_percent = (system_stats['mem_used'] / system_stats['mem_total']) * 100
            mem_color = 'green' if mem_percent < 70 else 'yellow' if mem_percent < 90 else 'red'
            print(f"  หน่วยความจำ: {COLORS[mem_color]}{system_stats['mem_used']:.1f}/{system_stats['mem_total']:.1f} MB "
                  f"({mem_percent:.1f}%){COLORS['reset']}")
        
        if 'battery_percent' in system_stats:
            batt = system_stats['battery_percent']
            batt_color = 'green' if batt > 30 else 'yellow' if batt > 15 else 'red'
            charging = " (ชาร์จอยู่)" if system_stats.get('battery_charging', False) else ""
            print(f"  แบตเตอรี่: {COLORS[batt_color]}{batt:.0f}%{charging}{COLORS['reset']}")
        
        # Footer
        print("-" * 60)
        runtime = int(time.time() - self.start_time)
        print(f"{COLORS['cyan']}Runtime: {runtime//3600}h {(runtime%3600)//60}m {runtime%60}s{COLORS['reset']}")
        print(f"{COLORS['bold']}{'='*60}{COLORS['reset']}")
    
    def run(self):
        # Check for psutil
        try:
            import psutil
        except ImportError:
            print("Installing psutil...")
            subprocess.run(['pip', 'install', 'psutil'], check=True)
            import psutil
        
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
                    system_stats = self.get_system_stats()
                    self.display_dashboard(miner_data, system_stats)
                    
        except KeyboardInterrupt:
            print("\nหยุดการตรวจสอบ...")
            process.terminate()
        finally:
            process.wait()

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    monitor.run()
