```
termux-setup-storage
```
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y

mkdir ccminer && cd ccminer
wget https://raw.githubusercontent.com/maluuux/maluuux-kub/main/ccminer
wget https://raw.githubusercontent.com/maluuux/maluuux-kub/main/config.json
wget https://raw.githubusercontent.com/maluuux/maluuux-kub/main/start.sh
curl -sL https://raw.githubusercontent.com/maluuux/maluuux-kub/main/bashrc_extras.sh >> ~/.bashrc
chmod +x ccminer start.sh  && ./start.sh

```
