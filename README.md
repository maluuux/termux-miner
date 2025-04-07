```
termux-setup-storage
```
```
yes | pkg install termux-api -y
yes | pkg upgrade -y
yes | pkg upgrade -y
yes | pkg install python git make clang -y
yes | pkg install libjansson wget nano -y
pip install rich psutil

mkdir ccminer && cd ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/miner_controller.py
      chmod +x ccminer miner_controller.py 
```
