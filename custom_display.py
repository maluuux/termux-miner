import subprocess
import re
import sys
from time import sleep

def colorize(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

def run_miner():
    cmd = [
        './ccminer',
        '-a', 'algo',
        '-o', 'pool_url:port',
        '-u', 'wallet_address',
        '-p', 'x'
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
            
        # ปรับแต่งการแสดงผลที่นี่
        if 'speed' in line.lower():
            # แยกค่าความเร็ว
            speed = re.search(r'(\d+\.\d+)\s*(kh/s|MH/s|H/s)', line)
            if speed:
                colored_speed = colorize(f"{speed.group(1)} {speed.group(2)}", 'cyan')
                print(f"⛏️ {colorize('Hashrate:', 'yellow')} {colored_speed}")
                
        elif 'accepted' in line.lower():
            print(colorize("✅ " + line.strip(), 'green'))
            
        elif 'rejected' in line.lower():
            print(colorize("❌ " + line.strip(), 'red'))
            
        else:
            print(line.strip())

if __name__ == "__main__":
    print(colorize("=== Custom CCminer Display ===", 'magenta'))
    print(colorize("Starting miner...", 'yellow'))
    run_miner()
