# 02. การตั้งค่า Google Colab เชื่อมต่อกับ Kali Linux

คู่มือทีละขั้นตอนในการเปิดใช้งาน Ollama บน Google Colab และเชื่อมต่อคำสั่งจาก Kali Linux VM

---

## ขั้นตอนที่ 1: เตรียม Google Colab

1. เข้าไปที่ [Google Colab](https://colab.research.google.com/)
2. สร้าง Notebook ใหม่ หรืออัปโหลดไฟล์ `colab_ollama_tunnel.ipynb`
3. ไปที่เมนู **Runtime** -> **Change runtime type**
4. เลือก **Hardware accelerator** เป็น **T4 GPU** แล้วกด **Save**

---

## ขั้นตอนที่ 2: รันโค้ดบน Colab

รันเซลล์โค้ดหลักเพื่อติดตั้ง Ollama, ดึงโมเดล, และเปิด Tunnel:

```python
# 1. ติดตั้ง Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# 2. เริ่มต้น Ollama Service ในเบื้องหลัง
!nohup ollama serve > ollama.log 2>&1 &
!sleep 4

# 3. โหลดโมเดลที่แนะนำ (Qwen2.5-Coder-14B Abliterated สำหรับงานสคริปต์)
!ollama pull huihui_ai/qwen2.5-coder-abliterated:14b

# 4. ติดตั้ง Cloudflare Tunnel
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
!dpkg -i cloudflared-linux-amd64.deb

# 5. เปิด Tunnel เชื่อมโยงพอร์ต 11434 สู่ Public URL
!cloudflared tunnel --url http://localhost:11434
```

> **สิ่งที่ต้องบันทึก:** ใน Output ของคำสั่งสุดท้าย คุณจะเห็นข้อความคล้าย:
> `https://your-unique-subdomain.trycloudflare.com`
> ให้คัดลอก URL นี้ไว้สำหรับนำไปใช้บน Kali Linux

---

## ขั้นตอนที่ 3: สั่งการจาก Kali Linux

### แบบที่ 1: ใช้คำสั่ง `curl` ทดสอบตรงๆ
เปิด Terminal บน Kali Linux แล้วพิมพ์คำสั่ง:

```bash
export AI_URL="https://your-unique-subdomain.trycloudflare.com"

# ทดสอบสอบถามคำสั่งวิเคราะห์
curl -s "$AI_URL/api/generate" -d '{
  "model": "huihui_ai/qwen2.5-coder-abliterated:14b",
  "prompt": "เขียนคำสั่ง Nmap เพื่อตรวจหาพอร์ตที่เปิดอยู่แบบเงียบๆ (SYN Stealth) พร้อมอธิบาย flag แต่ละตัว",
  "stream": false
}' | jq -r '.response'
```

### แบบที่ 2: ใช้สคริปต์ `ask.sh` ในโปรเจกต์
```bash
chmod +x client/ask.sh
./client/ask.sh -u "https://your-unique-subdomain.trycloudflare.com" "วิเคราะห์โครงสร้างคำสั่ง iptables สำหรับบล็อก port 22 ในแล็บ"
```

---

## การทำ Network Isolation สำหรับ Kali Lab
* เพื่อความปลอดภัยในขณะทดสอบ ให้แน่ใจว่า Virtual Machine (Kali/Windows/Arch) อยู่ใน Network โหมด **Host-Only** หรือ **Internal Network / NAT Network (Isolated)** 
* ไม่ควรให้ VM ที่กำลังทดสอบเชื่อมต่อตรงกับ Production Network ของบ้านหรือที่ทำงาน
