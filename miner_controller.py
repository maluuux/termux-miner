import subprocess
import re
from rich.console import Console
from rich.table import Table
from rich.live import Live
import time

console = Console()

def run_miner():
    process = subprocess.Popen(
        ['./ccminer', '-a', 'x16r', '-o', 'stratum+tcp://pool.example.com:3636', '-u', 'YOUR_WALLET', '-p', 'x'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    return process

def parse_output(line):
    """ประมวลผลข้อความจาก ccminer"""
    patterns = {
        'hashrate': re.compile(r'(\d+\.\d+) (kH|MH|GH)/s'),
        'accepted': re.compile(r'Accepted\s+:\s+(\d+)'),
        'rejected': re.compile(r'Rejected\s+:\s+(\d+)'),
        'gpu_stat': re.compile(r'GPU\s+#(\d+):\s+(\d+)\s+(\w+),\s+(\d+\.\d+)\s+(MH/s|kH/s)')
    }
    
    stats = {}
    for key, pattern in patterns.items():
        match = pattern.search(line)
        if match:
            stats[key] = match.groups()
    return stats

def display_dashboard(stats):
    """แสดงผลแบบ Dashboard สวยงาม"""
    table = Table(title="🚀 Miner Dashboard - Termux")
    table.add_column("GPU", style="cyan")
    table.add_column("ความเร็ว", style="green")
    table.add_column("สถานะ", style="magenta")
    
    if 'gpu_stat' in stats:
        for gpu in stats['gpu_stat']:
            table.add_row(f"GPU {gpu[0]}", f"{gpu[3]} {gpu[4]}", gpu[1])
    
    console.print(table)
    
    if 'hashrate' in stats:
        console.print(f"⚡ ความเร็วรวม: {stats['hashrate'][0]} {stats['hashrate'][1]}/s")
    if 'accepted' in stats:
        console.print(f"✅ รับแล้ว: {stats['accepted'][0]} | ❌ ปฏิเสธ: {stats.get('rejected', ['0'])[0]}")

def main():
    miner = run_miner()
    
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            line = miner.stdout.readline()
            if not line and miner.poll() is not None:
                break
                
            stats = parse_output(line)
            if stats:
                display_dashboard(stats)
                time.sleep(1)

if __name__ == "__main__":
    main()
