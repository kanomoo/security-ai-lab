# 03. การตั้งค่าบน Arch Linux และ Windows

คู่มือการนำ Client ไปใช้งานบน Arch Linux VM และ Windows VM

---

## 1. การใช้งานบน Arch Linux

Arch Linux เป็นระบบที่เหมาะสำหรับการตรวจสอบเชิงลึกและการวิเคราะห์เคอร์เนล/แพ็กเกจ

### ติดตั้งแพ็กเกจที่จำเป็น:
```bash
sudo pacman -Syu python python-requests jq curl
```

### การตั้งค่า Environment Variable:
คุณสามารถเพิ่ม URL ของ Colab Tunnel ไว้ใน `~/.bashrc` หรือ `~/.zshrc`:
```bash
export LLM_API_URL="https://your-subdomain.trycloudflare.com"
export LLM_MODEL="huihui_ai/qwen2.5-coder-abliterated:14b"
```

### ตัวอย่างการสั่งการ:
```bash
# ส่งโค้ด C หรือ config ไปวิเคราะห์หาช่องโหว่ความปลอดภัย
python3 client/ai_terminal.py -f /etc/ssh/sshd_config "ตรวจสอบการตั้งค่านี้ว่ามีจุดอ่อนด้านความปลอดภัยจุดใดบ้าง"
```

---

## 2. การใช้งานบน Windows

บน Windows สามารถใช้งานผ่าน **PowerShell** หรือโปรแกรม Chat GUI

### ผ่าน PowerShell:
1. เปิด PowerShell (กด Start พิมพ์ `powershell`)
2. เข้าไปที่โฟลเดอร์โปรเจกต์:
```powershell
cd "C:\Users\PC\Documents\New project\security-ai-lab\client"
.\ask.ps1 -Url "https://your-subdomain.trycloudflare.com" -Prompt "เขียน PowerShell script ตรวจสอบ Event ID 4625 (Failed Logon) ในแล็บ"
```

### ผ่านโปรแกรม GUI (เช่น Cherry Studio / Chatbox):
1. ดาวน์โหลด [Cherry Studio](https://cherry-studio.net/) หรือ [Chatbox](https://chatboxai.app/)
2. ในการตั้งค่า Model Provider:
   * เลือกประเภท: **Ollama**
   * กำหนด Base URL: `https://your-subdomain.trycloudflare.com`
   * กำหนด Model Name: `huihui_ai/qwen2.5-coder-abliterated:14b`
3. คุณจะได้หน้าจอแชตที่สวยงาม พร้อมจัดรูปแบบโค้ด Markdown อย่างชัดเจน
