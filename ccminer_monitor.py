#!/data/data/com.termux/files/usr/bin/python3
import subprocess
import re
import sys

def parse_ccminer_output(line):
    """Parse CCminer output and extract relevant information"""
    # ตัวอย่างการดักจับข้อมูลทั่วไปจาก CCminer
    speed_match = re.search(r'(\d+\.\d+) (kH|MH|GH)/s', line)
    accepted_match = re.search(r'(\d+)/(\d+) Accepted', line)
    rejected_match = re.search(r'(\d+) Rejected', line)
    gpu_match = re.search(r'GPU #\d+: (\d+\.\d+) (kH|MH|GH)/s', line)
    temp_match = re.search(r'T=(\d+)C', line)
    fan_match = re.search(r'F=(\d+)%', line)
    
    parsed_data = {}
    
    if speed_match:
        parsed_data['speed'] = speed_match.group(1)
        parsed_data['speed_unit'] = speed_match.group(2)
    
    if accepted_match:
        parsed_data['accepted'] = accepted_match.group(1)
        parsed_data['total'] = accepted_match.group(2)
    
    if rejected_match:
        parsed_data['rejected'] = rejected_match.group(1)
    
    if gpu_match:
        parsed_data['gpu_speed'] = gpu_match.group(1)
        parsed_data['gpu_speed_unit'] = gpu_match.group(2)
    
    if temp_match:
        parsed_data['temperature'] = temp_match.group(1)
    
    if fan_match:
        parsed_data['fan_speed'] = fan_match.group(1)
    
    return parsed_data

def display_custom_output(parsed_data):
    """Display mining information in custom format"""
    print("\033[2J\033[H")  # Clear screen (for Termux)
    print("=== Custom CCminer Monitor ===")
    print("===  Mining Information   ===")
    print("=============================")
    
    if 'speed' in parsed_data:
        print(f"Hash Rate: {parsed_data['speed']} {parsed_data['speed_unit']}/s")
    
    if 'gpu_speed' in parsed_data:
        print(f"GPU Speed: {parsed_data['gpu_speed']} {parsed_data['gpu_speed_unit']}/s")
    
    if 'accepted' in parsed_data:
        print(f"Accepted Shares: {parsed_data['accepted']}/{parsed_data['total']}")
    
    if 'rejected' in parsed_data:
        print(f"Rejected Shares: {parsed_data['rejected']}")
    
    if 'temperature' in parsed_data:
        print(f"Temperature: {parsed_data['temperature']}°C")
    
    if 'fan_speed' in parsed_data:
        print(f"Fan Speed: {parsed_data['fan_speed']}%")
    
    print("=============================")

def main():
    # เรียกใช้ start.sh และดักจับ output
    process = subprocess.Popen(
        ["./start.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    try:
        for line in iter(process.stdout.readline, ''):
            # Parse and display the output
            parsed_data = parse_ccminer_output(line)
            if parsed_data:  # Only display if we found relevant data
                display_custom_output(parsed_data)
            else:
                # You can print the original line if you want
                # print(line.strip())
                pass
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
