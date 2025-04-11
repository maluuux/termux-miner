#!/bin/bash
# ตรวจสอบว่าเป็น interactive shell และยังไม่ได้รัน autorun
if [[ $- == *i* ]] && [[ -z "$TERMUX_AUTORUN" ]]; then
    # ตรวจสอบว่ามีไฟล์ start.sh ในโฟลเดอร์ home
    if [[ -f ./run.sh ]]; then
        export TERMUX_AUTORUN=1
        bash ./run.sh
    fi
fi
