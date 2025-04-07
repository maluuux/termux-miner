```
termux-setup-storage
```
```
pkg update && pkg upgrade -y
pkg install python git -y
pip install --upgrade pip

git clone https://github.com/maluuux/termux-miner/blob/main/ccminer ~/ccminer
cd ~/ccminer
chmod +x ccminer
chmod +x run_miner.sh

```
