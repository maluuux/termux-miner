import subprocess
import re
import sys
from time import sleep

def format_hashrate(value, unit):
    """ปรับรูปแบบการแสดงผลแรงขุด"""
    units = {'kH': 'กิโล', 'MH': 'เมกะ', 'GH': 'กิกะ'}
    return f"⚡ แรงขุด: {value} {units.get(unit, unit)}ฮาช/วินาที ⚡"

def run_miner():
    process = subprocess.Popen(
        ['./ccminer'] + sys.argv[1:],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # ปรับแต่งการแสดงผล
            if 'accepted' in output:
                print(f"✅ {output.strip()}")
            elif 'rejected' in output:
                print(f"❌ {output.strip()}")
            elif 'hashrate' in output.lower():
                hashrate = re.search(r'(\d+\.\d+)\s*(kH|MH|GH)/s', output)
                if hashrate:
                    print(format_hashrate(hashrate.group(1), hashrate.group(2)))
            else:
                print(output.strip())

        sleep(0.1)

if __name__ == "__main__":
    print("🎛️ เริ่มระบบปรับแต่งการแสดงผลแรงขุด 🎛️")
    run_miner()
