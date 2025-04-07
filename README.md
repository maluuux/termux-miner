```
termux-setup-storage
```
```
yes | pkg upgrade -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
yes | pkg install git python make cmake binutils libtool autoconf automake -y

wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer -O ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json -O config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/custom_miner.py -O custom_miner.py
      chmod +x ccminer custom_miner.py
python custom_miner.py
```
