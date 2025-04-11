# เพิ่ม这部分ที่ท้ายไฟล์
if [[ $- == *i* ]] && [[ -z "$AUTORUN_DONE" ]]; then
    export AUTORUN_DONE=1
    if [[ -f ~/start.sh ]]; then
        echo "กำลังเริ่มสคริปต์ขุด..."
        termux-wake-lock  # ป้องกันโทรศัพท์หลับ
        bash ~/start.sh > ~/miner.log 2>&1 &
    fi
fi
