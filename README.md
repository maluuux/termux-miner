```
termux-setup-storage
```
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
yes | pkg install python git -y

wget https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/termux-miner/main/config.json
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/custom_miner.py
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/run_miner.sh
chmod +x config.json
chmod +x ccminer
chmod +x run_miner.sh
cd ~/ccminer
```
