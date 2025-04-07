```
termux-setup-storage
```
```
yes |pkg update && pkg upgrade -y
yes |pkg install python git -y

git clone https://github.com/maluuux/termux-miner/blob/main/ccminer ~/ccminer
cd ~/ccminer
chmod +x ccminer
chmod +x run_miner.sh

```
