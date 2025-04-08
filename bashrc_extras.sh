# Autorun only in interactive shell
if [[ $- == *i* ]]  && [ -z "$TERMUX_AUTORUN" ] && [chmod +x ccminer start.sh] && [ -f ~/ccminer/start.sh ]; then
    export TERMUX_AUTORUN=1
    bash ~/start.sh
fi
