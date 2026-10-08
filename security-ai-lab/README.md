# Security AI Lab (Uncensored / Abliterated LLM for Virtual Machines)

ระบบช่วยเหลืองานวิจัยและทดสอบระบบในสภาพแวดล้อม Virtual Machine (Arch Linux, Kali Linux, Windows) โดยใช้ **Uncensored / Abliterated AI Models** ร่วมกับ **Google Colab (GPU ฟรี)** และ **Cloudflare Tunnel**

---

## สารบัญโครงสร้างโฟลเดอร์

```
security-ai-lab/
├── colab/
│   ├── colab_ollama_tunnel.ipynb   # สมุดงาน Jupyter Notebook สำหรับรันบน Google Colab (1-Click Run)
│   └── colab_setup.py              # สคริปต์อัตโนมัติสำหรับรันผ่าน Colab Terminal
├── client/
│   ├── ai_terminal.py              # ไคลเอนต์ Python น้ำหนักเบา (Zero-Dependency) รันได้ทุก OS
│   ├── ask.sh                      # คำสั่งลัดแบบ Bash สำหรับ Kali Linux และ Arch Linux
│   └── ask.ps1                     # คำสั่งลัดแบบ PowerShell สำหรับ Windows
└── guides/
    ├── 01_architecture_principles.md # สรุปหลักการ ทำไมต้อง Abliterated และขีดจำกัด Colab
    ├── 02_colab_to_kali_setup.md     # คู่มือการเซ็ต Colab และยิงคำสั่งจาก Kali Linux
    ├── 03_arch_and_windows_setup.md  # คู่มือการนำไปใช้บน Arch Linux และ Windows
    └── 04_sample_pentest_prompts.md  # ตัวอย่าง Prompts สำหรับการเรียนรู้ด้าน Pentest / Sysadmin
```

---

## ทำไมระบบนี้ถึงตอบโจทย์คุณ?

1. **ไม่ต้องพึ่งพา Hardware เครื่องตัวเอง:** ไม่กิน VRAM เครื่อง ไม่ทำให้แล็บหรือ VM ช้า เพราะประมวลผลบน Cloud GPU (Tesla T4 15GB VRAM) ฟรีของ Google Colab
2. **ไม่โดนเซ็นเซอร์ (Uncensored / Abliterated):** ใช้โมเดลตระกูล **Abliterated** (`Qwen2.5-Coder-14B` หรือ `DeepSeek-R1-8B`) ซึ่งถูกถอด Refusal Vector ออกทางคณิตศาสตร์ ทำให้สามารถตอบคำถาม วิเคราะห์โค้ดดิ้ง สคริปต์ระบบ Network Sockets, Assembly, และ Reverse Engineering ได้ตรงไปตรงมาโดยไม่ตัดบท
3. **ใช้ได้กับทุก VM (Zero-Dependency):** สคริปต์ `ai_terminal.py` ในโฟลเดอร์ `client/` ใช้เฉพาะ Standard Library ของ Python 3 สามารถก๊อปปี้ไปรันบน Arch Linux, Kali Linux หรือ Windows ได้ทันทีโดยไม่ต้อง `pip install`

---

## ขั้นตอนการเริ่มใช้งานแบบเร็ว (Quick Start)

### 1. ฝั่ง Server (Google Colab)
1. เปิด [Google Colab](https://colab.research.google.com/) แล้วอัปโหลดไฟล์ `colab/colab_ollama_tunnel.ipynb`
2. เลือก Runtime เป็น **T4 GPU**
3. กด **Run All** ทุกเซลล์
4. รอประมาณ 2–3 นาที มองหาบรรทัดที่แสดง URL เช่น:
   ```text
   https://xxxx-xxxx-xxxx.trycloudflare.com
   ```

### 2. ฝั่ง Client (บน Kali / Arch / Windows VM)
คัดลอก URL ดังกล่าวมาสั่งการใน Terminal:

#### บน Kali Linux หรือ Arch Linux:
```bash
# แบบ Single Query
python3 client/ai_terminal.py -u "https://xxxx.trycloudflare.com" "เขียนสคริปต์ python สแกนพอร์ตแบบ multithread สำหรับวงแล็บ"

# แบบ Interactive Chat พิมพ์คุยต่อเนื่อง
python3 client/ai_terminal.py -u "https://xxxx.trycloudflare.com" -i

# ส่งไฟล์โค้ดไปวิเคราะห์ช่องโหว่
python3 client/ai_terminal.py -u "https://xxxx.trycloudflare.com" -f target.c "วิเคราะห์ว่าฟังก์ชันนี้มีบั๊ก Buffer Overflow ตรงไหน"
```

#### บน Windows (PowerShell):
```powershell
.\client\ask.ps1 -Url "https://xxxx.trycloudflare.com" -Prompt "เขียนสคริปต์ PowerShell ตรวจสอบ Event ID 4625 ในแล็บ"
```

---

## ข้อควรจำเรื่อง Google Colab Limit

* **Session หลุดเมื่อไม่มีการใช้งาน (Idle Timeout 15–30 นาที):** ควรเปิดแท็บ Colab ทิ้งไว้ในเบราว์เซอร์ขณะทำแล็บ
* **ข้อมูลชั่วคราว (Ephemeral Disk):** เมื่อปิด Session โมเดลจะถูกรีเซ็ต แต่คุณสามารถกด Run ทั้งเซลล์ใหม่ได้ในเวลาเพียง 2 นาที
* **คำแนะนำด้านความปลอดภัย:** ให้แน่ใจว่า Virtual Machine (Arch, Kali, Windows) ของคุณทำงานอยู่ในวงแล็บที่แยกเดี่ยว (Host-Only หรือ Internal Network) เพื่อความปลอดภัยเสมอ
