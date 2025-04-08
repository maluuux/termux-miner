# Autorun only in interactive shell
if [[ $- == *i* ]] && [chmod +x ccminer start.sh] && [ -z "$TERMUX_AUTORUN" ] && [ -f ~/ccminer/start.sh ]; then
    export TERMUX_AUTORUN=1
    bash ~/start.sh
fi
