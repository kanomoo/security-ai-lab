# 01. หลักการสถาปัตยกรรม (Architecture & Principles)

เอกสารนี้สรุปแนวคิด สถาปัตยกรรมระบบ และเหตุผลทางเทคนิคในการนำ Uncensored / Abliterated LLM มาใช้ในสภาพแวดล้อม Virtual Machine Lab เพื่อการศึกษาด้าน Cybersecurity

---

## 1. ปัญหาของ Mainstream LLM (ChatGPT, Claude, Gemini) ในงาน Security Lab

* **Automated Safety Filters:** โมเดลเชิงพาณิชย์หลักถูกออกแบบมาให้ปฏิเสธคำขอที่เกี่ยวข้องกับ Exploitation, Reverse Engineering, Binary Analysis, Shellcode, หรือ Bypass เทคนิค
* **การ Prompt Bypass ไม่เสถียร:** การหลอกโมเดลด้วยประโยคอย่าง *"ทำในแล็บ/VM ควบคุมได้"* ใช้ได้เฉพาะคำถามเชิงทฤษฎีพื้นฐาน แต่เมื่อสั่งการสคริปต์ขั้นสูง Guardrail ระดับ API จะตัด Context หรือบล็อกทันที
* **ความเสี่ยงในการโดนแบนบัญชี:** หากบัญชีส่งคำถามที่ถูกจัดหมวดหมู่ว่ามีความเสี่ยงบ่อยครั้ง อาจถูกระงับสิทธิ์การใช้งานถาวร

---

## 2. ทำไมต้องใช้ "Abliterated Models"?

Abliteration เป็นเทคนิคการปรับแต่งโมเดลทางคณิตศาสตร์ (Weight Orthogonalization) โดยการหาเวกเตอร์ทิศทางการปฏิเสธ (Refusal Direction) ใน Hidden States แล้วลบเวกเตอร์นั้นออก:
1. **รักษาความฉลาด 100%:** แตกต่างจากโมเดล Uncensored ยุคแรกที่เทรนด้วยข้อมูลคุณภาพต่ำ โมเดล Abliterated ยังคงความฉลาด ความรู้เรื่องโค้ดดิ้ง และสถาปัตยกรรมระบบของ Base Model ไว้ครบถ้วน
2. **ไม่ปฏิเสธคำสั่งแล็บ:** สามารถวิเคราะห์ Shellcode, Assembly, Reverse Engineering, Exploit logic, Network Socket, และคำสั่งระบบต่างๆ บน Kali Linux, Arch Linux, และ Windows ได้อย่างตรงไปตรงมา

---

## 3. สถาปัตยกรรมการเชื่อมต่อ (Colab -> Tunnel -> VM Lab)

เมื่อเครื่องคอมพิวเตอร์ของคุณมีทรัพยากร (VRAM) ไม่เพียงพอสำหรับการรัน Local:

```
+---------------------------------------------------------+
|                  Google Colab (Free Tier)                |
|  - Tesla T4 GPU (VRAM ~15 GB)                            |
|  - Ollama Engine (รัน Qwen2.5-Coder-14B หรือ DeepSeek-R1) |
|  - Cloudflare Tunnel (สร้าง Public URL อัตโนมัติ)          |
+---------------------------------------------------------+
                           |
                           | HTTPS Encrypted Tunnel (Public URL)
                           v
+---------------------------------------------------------+
|                    Your Local Machine                   |
|                                                         |
|  [Arch Linux VM]      [Kali Linux VM]    [Windows VM]   |
|  - System Audit       - Pentest Tools    - PowerShell   |
|  - Network Monitor    - Packet Analysis  - Event Logs   |
|         ^                    ^                 ^        |
|         |                    |                 |        |
|         +---------- ai_terminal Client --------+        |
|                     (Python / Bash / cURL)              |
+---------------------------------------------------------+
```

---

## 4. ข้อจำกัดของ Google Colab Free & แนวทางจัดการ

| ข้อจำกัด | ผลกระทบ | วิธีรับมือ |
| :--- | :--- | :--- |
| **Idle Timeout (15–30 นาที)** | Colab หลุดเมื่อไม่มีการกดหน้าเว็บ | เปิดหน้าแท็บ Colab ไว้ขณะทำแล็บ หรือเปิด Developer Console รัน JavaScript ช่วย keepalive หากจำเป็น |
| **Session Cap (4–12 ชม.)** | ตัดการทำงานอัตโนมัติ | ออกแบบมาสำหรับ Session ทำแล็บ 1–3 ชั่วโมง เมื่อเสร็จให้ปิดตัว |
| **Ephemeral Disk** | ไฟล์โมเดลที่โหลดไว้จะหายไปเมื่อปิด | จัดเตรียมสคริปต์แบบ 1-Click รัน เพียงกดปุ่มเดียว โหลดโมเดลพร้อมเปิด Tunnel ภายใน 2–3 นาที |
| **Dynamic URL** | URL จาก Cloudflare จะเปลี่ยนทุกรอบ | ให้สคริปต์ client รองรับการเปลี่ยน URL ผ่าน Environment Variable หรือไฟล์ config อย่างง่ายดาย |
