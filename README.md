
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
mkdir ccminer && cd ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/run.sh
curl -sL https://raw.githubusercontent.com/maluuux/termux-miner/main/bashrc_extras.sh >> ~/.bashrc
chmod +x ccminer start.sh  && ./start.sh

```
