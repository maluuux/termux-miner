```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
pkg update
pkg install python git make clang
pip install rich psutil
mkdir ccminer && cd ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh
      chmod +x ccminer start.sh && ./start.sh
```
