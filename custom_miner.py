#!/usr/bin/env python3
import subprocess
import json
import re
import time
from colorama import init, Fore
from rich.console import Console
from rich.panel import Panel

# Initialize
init()
console = Console()

# Custom UI
def show_header(config):
    title = f"[bold cyan]CCminer - {config['algorithm'].upper()}[/bold cyan]"
    subtitle = f"[green]Pool: {config['pool']}[/green]"
    console.print(Panel.fit(title, subtitle=subtitle))

# Parse Output
def parse_output(line, config):
    custom = config["custom_output"]
    if "accepted" in line.lower() and custom["show_accepted"]:
        return f"[green]✓ {line.strip()}[/green]"
    elif "rejected" in line.lower() and custom["show_rejected"]:
        return f"[red]✗ {line.strip()}[/red]"
    elif "hashrate" in line.lower() and custom["show_hashrate"]:
        hashrate = re.search(r"(\d+\.\d+) (kH|MH|H)/s", line)
        if hashrate:
            return f"[yellow]⚡ Hashrate: {hashrate.group(1)} {hashrate.group(2)}/s[/yellow]"
    return None  # ไม่แสดงบรรทัดที่ไม่ต้องการ

# Main Function
def start_mining():
    config = load_config()
    show_header(config)
    
    cmd = [
        "./ccminer",
        "-a", config["algorithm"],
        "-o", config["pool"],
        "-u", config["wallet"],
        "-p", config["password"],
        "-i", str(config["intensity"]),
        "-t", str(config["threads"])
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    try:
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                parsed = parse_output(line, config)
                if parsed:
                    console.print(parsed)
    except KeyboardInterrupt:
        console.print("[red]Stopping miner...[/red]")
        process.terminate()

if __name__ == "__main__":
    start_mining()
