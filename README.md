```
termux-setup-storage
```
```
yes | pkg upgrade -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
pkg install git python make cmake binutils libtool autoconf automake -y
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/custom_miner.py
wget  https://raw.githubusercontent.com/maluuux/termux-miner/run_miner.sh
      chmod +x ccminer run_miner.sh && python custom_miner.py
```
