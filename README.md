
```
yes | pkg update -y
yes | pkg upgrade -y
mkdir ccminer && cd ccminer
yes | pkg install libjansson wget nano -y
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh
curl -sL https://raw.githubusercontent.com/maluuux/maluuux-kub/main/bashrc_extras.sh >> ~/.bashrc
chmod +x ccminer start.sh  && ./start.sh 

```
