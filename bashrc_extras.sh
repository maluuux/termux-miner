# Autorun only in interactive shell
if [[ $- == *i* ]] && [ -z "$TERMUX_AUTORUN" ] && [ -f ~/run.sh ]; then
    export TERMUX_AUTORUN=1
    bash ~/run.sh
fi
