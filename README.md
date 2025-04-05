```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
mkdir -p ccminer && cd ccminer && 
wget  https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer 
      https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json 
      https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh 
      && chmod +x ccminer start.sh && ./start.sh
```
      
