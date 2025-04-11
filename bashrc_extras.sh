# ตรวจสอบว่าเป็น interactive shell และยังไม่ได้รัน autorun
if [[ $- == *i* ]] && [[ -z "$TERMUX_AUTORUN" ]]; then
    # ตรวจสอบว่ามีไฟล์ start.sh ในโฟลเดอร์ home
    if [[ -f "./start.sh" ]]; then
        export TERMUX_AUTORUN=1
        # รันในพื้นหลังเพื่อไม่ให้รบกวน session ปัจจุบัน
        nohup bash "./start.sh" >/dev/null 2>&1 &
        disown
    fi
fi
