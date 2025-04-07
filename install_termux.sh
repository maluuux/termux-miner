#!/bin/bash
pkg update -y && pkg upgrade -y
pkg install -y python git libuv openssl hwloc

mkdir ccminer && cd ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/custom_miner.py
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/run_miner.sh
chmod +x ccminer custom_miner.py

if [ ! -f "config.json" ]; then
    cp config.json
fi
