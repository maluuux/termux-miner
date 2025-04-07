```
termux-setup-storage
```
```
pkg install termux-api
pkg update
pkg install python git make clang
pip install rich psutil

yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y


mkdir ccminer && cd ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/miner_controller.py
      chmod +x ccminer start.sh miner_controller.py && ./start.sh
```
