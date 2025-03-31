import os
import time
import tkinter as tk
import threading
import webbrowser  # ใช้เปิดลิงก์ในเว็บเบราว์เซอร์

def get_entry_value(entry):
    """ดึงค่าจากช่องกรอก ถ้าเว้นว่างไว้ให้เป็น 0"""
    value = entry.get().strip()  # ตัดช่องว่างหน้า-หลัง
    return int(value) if value.isdigit() else 0  # ถ้าไม่มีค่าให้ใช้ 0

def shutdown():
    """เริ่มนับถอยหลังและแสดงเวลาบน UI"""
    global countdown_running, remaining_time
    
    # ดึงค่าจากช่องกรอก ถ้าไม่กรอกอะไรเลย = 0
    hours = get_entry_value(hour_entry) * 3600
    minutes = get_entry_value(minute_entry) * 60
    seconds = get_entry_value(second_entry)
    remaining_time = hours + minutes + seconds  # รวมเวลาทั้งหมดเป็นวินาที

    if remaining_time == 0:
        status_label.config(text="❌ กรุณากรอกเวลาให้มากกว่า 0 วินาที")
        return

    countdown_running = True
    status_label.config(text=f"🔵 คอมพิวเตอร์จะปิดใน {remaining_time} วินาที")
    update_countdown()  # เริ่มแสดงเวลานับถอยหลัง

    # รันคำสั่งปิดเครื่องหลังจากเวลานับถอยหลังจบลง
    def shutdown_after_delay():
        time.sleep(remaining_time)
        if countdown_running:
            os.system("shutdown /s /t 0")

    threading.Thread(target=shutdown_after_delay, daemon=True).start()

def update_countdown():
    """อัปเดตเวลานับถอยหลังแบบเรียลไทม์บน UI"""
    global remaining_time, countdown_running
    if remaining_time > 0 and countdown_running:
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        countdown_label.config(text=f"⏳ เวลาที่เหลือ: {hours} ชม. {minutes} นาที {seconds} วินาที")
        remaining_time -= 1
        root.after(1000, update_countdown)  # เรียกตัวเองซ้ำทุก 1 วินาที
    elif remaining_time <= 0:
        countdown_label.config(text="🔴 ปิดเครื่องแล้ว!")
        status_label.config(text="🛑 คอมพิวเตอร์กำลังปิด...")

def cancel_shutdown():
    """ยกเลิกการปิดเครื่อง"""
    global countdown_running
    countdown_running = False
    os.system("shutdown /a")  # คำสั่งยกเลิกการปิดเครื่อง Windows
    countdown_label.config(text="✅ ยกเลิกการปิดเครื่อง")
    status_label.config(text="🔵 การปิดเครื่องถูกยกเลิกแล้ว")

def open_link():
    """เปิดเว็บเบราว์เซอร์ไปยังลิงก์ที่กำหนด"""
    webbrowser.open("https://nattapat2871.online")  # 🔗 เปลี่ยนเป็นลิงก์ของคุณเอง

# สร้างหน้าต่าง UI
root = tk.Tk()
root.title("ตัวตั้งเวลาปิดเครื่อง")
root.geometry("350x280")  # ปรับขนาดหน้าต่างให้มีที่ว่างพอลิงก์

# ตัวแปรเก็บสถานะ
countdown_running = False
remaining_time = 0

# ส่วนของ UI
tk.Label(root, text="ตั้งเวลาปิดเครื่อง:").pack(pady=5)

frame = tk.Frame(root)
frame.pack()

# ช่องกรอก ชั่วโมง / นาที / วินาที
hour_entry = tk.Entry(frame, width=5)
hour_entry.pack(side=tk.LEFT)
tk.Label(frame, text="ชั่วโมง").pack(side=tk.LEFT, padx=5)

minute_entry = tk.Entry(frame, width=5)
minute_entry.pack(side=tk.LEFT)
tk.Label(frame, text="นาที").pack(side=tk.LEFT, padx=5)

second_entry = tk.Entry(frame, width=5)
second_entry.pack(side=tk.LEFT)
tk.Label(frame, text="วินาที").pack(side=tk.LEFT, padx=5)

btn_start = tk.Button(root, text="เริ่มนับถอยหลัง", command=shutdown, bg="green", fg="white")
btn_start.pack(pady=5)

btn_cancel = tk.Button(root, text="ยกเลิกการปิดเครื่อง", command=cancel_shutdown, bg="red", fg="white")
btn_cancel.pack(pady=5)

# แสดงเวลานับถอยหลัง
countdown_label = tk.Label(root, text="", font=("Arial", 14))
countdown_label.pack(pady=10)

# แสดงสถานะ
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=5)

# 🔗 ลิงก์ที่มุมขวาล่าง
link_label = tk.Label(root, text="ดูรายละเอียดเพิ่มเติม", fg="blue", cursor="hand2")
link_label.pack(side=tk.BOTTOM, anchor="se", padx=10, pady=5)
link_label.bind("<Button-1>", lambda e: open_link())  # กดแล้วเปิดเว็บ

# เริ่มต้นโปรแกรม
root.mainloop()
