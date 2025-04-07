# Autorun only in interactive shell
if [[ $- == *i* ]] && [ -z "$TERMUX_AUTORUN" ] && [ -f ~/ccminer/start.sh ]; then
    export TERMUX_AUTORUN=1
    bash ~/ccminer/start.sh
fi
