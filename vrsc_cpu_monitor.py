import subprocess
import re
import sys
import time
import psutil

def parse_miner_output(line):
    """Parse output for VRSC CPU mining"""
    patterns = {
        'hashrate': re.compile(r'(\d+\.\d+)\s*(H|kH|MH|GH)/s'),
        'accepted': re.compile(r'accepted:\s*(\d+)/'),
        'rejected': re.compile(r'rejected:\s*(\d+)'),
        'cpu_usage': re.compile(r'CPU:\s*(\d+)%'),
        'shares': re.compile(r'shares:\s*(\d+)\/(\d+)'),
        'difficulty': re.compile(r'difficulty\s*(\d+\.\d+)'),
        'block': re.compile(r'block:\s*(\d+)'),
        'uptime': re.compile(r'uptime:\s*(\d+d)?\s*(\d+h)?\s*(\d+m)?')
    }
    
    results = {}
    for key, pattern in patterns.items():
        match = pattern.search(line.lower())  # ใช้ lower() เพื่อให้ไม่สนใจตัวพิมพ์เล็กใหญ่
        if match:
            if key == 'hashrate':
                value = float(match.group(1))
                unit = match.group(2)
                # Convert to H/s for consistency
                if unit == 'kH':
                    value *= 1000
                elif unit == 'MH':
                    value *= 1000000
                elif unit == 'GH':
                    value *= 1000000000
                results[key] = value
                results['hashrate_unit'] = 'H/s'
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
            else:
                results[key] = match.group(1)
    
    return results

def get_cpu_stats():
    """Get CPU temperature and usage (may not work on all Android devices)"""
    stats = {}
    try:
        # อุณหภูมิ CPU (อาจไม่ทำงานบนทุกอุปกรณ์)
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000
            stats['cpu_temp'] = temp
        
        # การใช้งาน CPU
        stats['cpu_usage'] = psutil.cpu_percent(interval=1)
        stats['cpu_cores'] = psutil.cpu_count(logical=False)
        stats['cpu_freq'] = psutil.cpu_freq().current if hasattr(psutil, 'cpu_freq') else None
    except:
        pass
    
    return stats

def display_cpu_mining_output(miner_data):
    """Display CPU mining information in custom format"""
    # ANSI color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Clear screen and move cursor to top-left
    print("\033[2J\033[H", end="")
    
    # Get CPU stats
    cpu_stats = get_cpu_stats()
    
    print(f"{BOLD}{CYAN}=== VerusCoin (VRSC) CPU Mining Monitor ==={RESET}")
    print(f"{BLUE}⛏️ การขุดด้วย CPU บน Android{RESET}")
    print("-" * 50)
    
    # แสดงข้อมูลการขุด
    if 'hashrate' in miner_data:
        hashrate = miner_data['hashrate']
        if hashrate >= 1000000:  # ถ้ามากกว่า 1MH/s
            display_hash = f"{hashrate/1000000:.2f} MH/s"
        elif hashrate >= 1000:   # ถ้ามากกว่า 1kH/s
            display_hash = f"{hashrate/1000:.2f} kH/s"
        else:
            display_hash = f"{hashrate:.2f} H/s"
        
        color = GREEN if hashrate > 1000 else YELLOW if hashrate > 100 else RED
        print(f"{BOLD}ความเร็วการขุด:{RESET} {color}{display_hash}{RESET}")
    
    if 'accepted' in miner_data or 'rejected' in miner_data:
        accepted = miner_data.get('accepted', 0)
        rejected = miner_data.get('rejected', 0)
        total = accepted + rejected
        ratio = (accepted / total * 100) if total > 0 else 100
        ratio_color = GREEN if ratio > 95 else YELLOW if ratio > 80 else RED
        print(f"{BOLD}Shares:{RESET} {GREEN}{accepted} ยอมรับ{RESET} | {RED}{rejected} ปฏิเสธ{RESET} | {ratio_color}({ratio:.1f}%){RESET}")
    
    if 'difficulty' in miner_data:
        print(f"{BOLD}ความยาก:{RESET} {miner_data['difficulty']:.2f}")
    
    if 'block' in miner_data:
        print(f"{BOLD}บล็อกที่พบ:{RESET} {miner_data['block']}")
    
    if 'uptime' in miner_data:
        print(f"{BOLD}ระยะเวลาการขุด:{RESET} {miner_data['uptime']}")
    
    print("-" * 50)
    
    # แสดงข้อมูล CPU
    print(f"{BOLD}=== ข้อมูล CPU ==={RESET}")
    if 'cpu_temp' in cpu_stats:
        temp_color = GREEN if cpu_stats['cpu_temp'] < 60 else YELLOW if cpu_stats['cpu_temp'] < 70 else RED
        print(f"{BOLD}อุณหภูมิ CPU:{RESET} {temp_color}{cpu_stats['cpu_temp']:.1f}°C{RESET}")
    
    if 'cpu_usage' in cpu_stats:
        usage_color = GREEN if cpu_stats['cpu_usage'] < 70 else YELLOW if cpu_stats['cpu_usage'] < 90 else RED
        print(f"{BOLD}การใช้งาน CPU:{RESET} {usage_color}{cpu_stats['cpu_usage']}%{RESET}")
    
    if 'cpu_cores' in cpu_stats:
        print(f"{BOLD}จำนวน cores:{RESET} {cpu_stats['cpu_cores']}")
    
    if 'cpu_freq' in cpu_stats and cpu_stats['cpu_freq']:
        print(f"{BOLD}ความถี่ CPU:{RESET} {cpu_stats['cpu_freq']/1000:.1f} GHz")
    
    print("-" * 50)
    print(f"{YELLOW}อัปเดตล่าสุด: {time.strftime('%H:%M:%S')}{RESET}")
    print(f"{BOLD}=========================================={RESET}")

def main():
    # ตรวจสอบว่า psutil ติดตั้งหรือยัง
    try:
        import psutil
    except ImportError:
        print("กำลังติดตั้ง psutil...")
        subprocess.run(['pip', 'install', 'psutil'], check=True)
        import psutil
    
    # เรียกใช้สคริปต์ start.sh และดักจับ output
    process = subprocess.Popen(
        ["./start.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    try:
        for line in iter(process.stdout.readline, ''):
            # วิเคราะห์และแสดงผลแบบกำหนดเองเท่านั้น
            miner_data = parse_miner_output(line)
            if miner_data:
                display_cpu_mining_output(miner_data)
                
    except KeyboardInterrupt:
        print(f"\n{BOLD}หยุดการตรวจสอบ...{RESET}")
        process.terminate()
    finally:
        process.wait()

if __name__ == "__main__":
    main()
