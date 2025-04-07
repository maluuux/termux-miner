```
termux-setup-storage
```
```
yes |pkg update && pkg upgrade -y
yes |pkg install python git -y

git clone https://github.com/maluuux/termux-miner/blob/main/config.json
git clone https://github.com/maluuux/termux-miner/blob/main/custom_miner.py
git clone https://github.com/maluuux/termux-miner/blob/main/run_miner.sh
git clone https://github.com/maluuux/termux-miner/blob/main/ccminer
chmod +x ccminer
chmod +x run_miner.sh
cd ~/ccminer
```
