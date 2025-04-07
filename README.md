```
termux-setup-storage
```
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
yes | pkg install python git -y

wget https://raw.githubusercontent.com/termux-miner/blob/main/config.json
wget https://raw.githubusercontent.com/termux-miner/blob/main/custom_miner.py
wget https://raw.githubusercontent.com/termux-miner/blob/main/run_miner.sh
wget https://raw.githubusercontent.comtermux-miner/blob/main/ccminer
chmod +x config.json
chmod +x ccminer
chmod +x run_miner.sh
cd ~/ccminer
```
