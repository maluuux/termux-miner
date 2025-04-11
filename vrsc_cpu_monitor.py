import subprocess
import re
import time
import psutil
from datetime import datetime

class VrscCpuMinerMonitor:
    def __init__(self):
        self.hashrate_history = []
        self.start_time = time.time()
        self.max_history = 30
        
    def get_system_stats(self):
        """Get system stats with fallback options"""
        stats = {}
        
        # CPU Temperature (try multiple paths)
        temp_paths = [
            '/sys/class/thermal/thermal_zone0/temp',
            '/sys/class/thermal/thermal_zone1/temp',
            '/sys/devices/virtual/thermal/thermal_zone0/temp'
        ]
        
        for path in temp_paths:
            try:
                with open(path, 'r') as f:
                    stats['cpu_temp'] = float(f.read()) / 1000
                    break
            except:
                continue
        
        # CPU Usage (always available)
        stats['cpu_usage'] = psutil.cpu_percent(interval=1)
        stats['cpu_cores'] = psutil.cpu_count(logical=False)
        
        # Memory (always available)
        mem = psutil.virtual_memory()
        stats['mem_used'] = mem.used / (1024**2)  # MB
        stats['mem_total'] = mem.total / (1024**2)  # MB
        
        # Battery (may not be available)
        try:
            battery = psutil.sensors_battery()
            if battery:
                stats['battery_percent'] = battery.percent
                stats['battery_charging'] = battery.power_plugged
        except:
            pass
            
        return stats

    def display_dashboard(self, miner_data, system_stats):
        """Display dashboard with fallback for missing system stats"""
        COLORS = {
            'green': '\033[92m', 'yellow': '\033[93m', 'red': '\033[91m',
            'blue': '\033[94m', 'cyan': '\033[96m', 'purple': '\033[95m',
            'reset': '\033[0m', 'bold': '\033[1m'
        }
        
        print("\033[2J\033[H", end="")
        print(f"{COLORS['bold']}{COLORS['purple']}=== VRSC CPU Mining Dashboard ==={COLORS['reset']}")
        print("-" * 60)
        
        # Mining Status (เหมือนเดิม)
        
        # System Status Section
        print(f"\n{COLORS['bold']}🖥️ สถานะระบบ:{COLORS['reset']}")
        
        if not system_stats:
            print(f"  {COLORS['yellow']}⚠️ ไม่สามารถอ่านข้อมูลระบบบางส่วนได้{COLORS['reset']}")
        
        # CPU Info (จะแสดงเสมอ)
        print(f"  การใช้ CPU: {system_stats.get('cpu_usage', 'N/A')}%")
        print(f"  จำนวน Cores: {system_stats.get('cpu_cores', 'N/A')}")
        
        # CPU Temperature (ถ้ามี)
        if 'cpu_temp' in system_stats:
            temp = system_stats['cpu_temp']
            temp_color = 'green' if temp < 60 else 'yellow' if temp < 70 else 'red'
            print(f"  อุณหภูมิ CPU: {COLORS[temp_color]}{temp:.1f}°C{COLORS['reset']}")
        else:
            print(f"  อุณหภูมิ CPU: {COLORS['yellow']}ไม่สามารถอ่านค่า{COLORS['reset']}")
        
        # Memory (จะแสดงเสมอ)
        mem_percent = (system_stats['mem_used'] / system_stats['mem_total']) * 100
        mem_color = 'green' if mem_percent < 70 else 'yellow' if mem_percent < 90 else 'red'
        print(f"  หน่วยความจำ: {COLORS[mem_color]}{system_stats['mem_used']:.1f}/{system_stats['mem_total']:.1f} MB "
              f"({mem_percent:.1f}%){COLORS['reset']}")
        
        # Battery (ถ้ามี)
        if 'battery_percent' in system_stats:
            batt = system_stats['battery_percent']
            batt_color = 'green' if batt > 30 else 'yellow' if batt > 15 else 'red'
            charging = " (ชาร์จอยู่)" if system_stats.get('battery_charging', False) else ""
            print(f"  แบตเตอรี่: {COLORS[batt_color]}{batt:.0f}%{charging}{COLORS['reset']}")
        else:
            print(f"  แบตเตอรี่: {COLORS['yellow']}ไม่สามารถอ่านค่า{COLORS['reset']}")
        
        print("-" * 60)

if __name__ == "__main__":
    monitor = VrscCpuMinerMonitor()
    
    # Test system stats
    system_stats = monitor.get_system_stats()
    print("Testing system stats reading:")
    print(system_stats)
    
    # Run with dummy miner data
    monitor.display_dashboard(
        miner_data={'hashrate': 1500, 'accepted': 10, 'rejected': 1},
        system_stats=system_stats
    )
