```
termux-setup-storage
```
```bash
bash <(curl -s https://raw.githubusercontent.com/[USER]/ccminer-termux/main/install_termux.sh)

```
yes | pkg upgrade -y
yes | pkg upgrade -y
yes | pkg install git python make cmake binutils libtool autoconf automake -y
yes | pkg install libjansson wget nano -y

mkdir ccminer && cd ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget  https://raw.githubusercontent.com/maluuux/termux-miner/custom_miner.py
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/staer.sh
      chmod +x ccminer custom_miner.py config.json
```
