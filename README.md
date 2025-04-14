
```
termux-setup-storage
```
```
yes | pkg update -y
yes | pkg upgrade -y
yes | pkg install libjansson wget nano -y
yes | pkg install python -y
pip install --upgrade pip wheel
pip install psutil --no-binary psutil
mkdir ccminer && cd ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/ccminer
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/config.json
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/start.sh
wget https://raw.githubusercontent.com/maluuux/termux-miner/main/vrsc_cpu_monitor.py
curl -sL  https://raw.githubusercontent.com/maluuux/termux-miner/main/bashrc_extras.sh >> ~/.bashrc
chmod +x vrsc_cpu_monitor.py
chmod +x ccminer start.sh &&  python vrsc_cpu_monitor.py
```
```
python vrsc_cpu_monitor.py
```
