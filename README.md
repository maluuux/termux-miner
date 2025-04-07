```
termux-setup-storage
```
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
yes | pkg install python git -y

git clone https://github.com/maluuux/termux-miner/termux-miner/main/config.json
git clone https://github.com/maluuux/termux-miner/main/custom_miner.py
git clone https://github.com/maluuux/termux-miner/main/run_miner.sh
git clone https://github.com/maluuux/termux-miner/main/ccminer
chmod +x config.json
chmod +x ccminer
chmod +x run_miner.sh
cd ~/ccminer
```
