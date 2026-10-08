# Security AI Lab Project

ชุดเครื่องมือและคู่มือสำหรับการนำ **Uncensored / Abliterated LLM** มาช่วยในการศึกษา วิจัย และทดสอบระบบความปลอดภัย (Cybersecurity, System Administration, Pentesting Lab) บนสภาพแวดล้อม **Arch Linux**, **Kali Linux**, และ **Windows Virtual Machines**

---

## สารบัญโฟลเดอร์หลัก

* **[`security-ai-lab/`](file:///C:/Users/PC/Documents/New%20project/security-ai-lab/)**
  * **[`colab/`](file:///C:/Users/PC/Documents/New%20project/security-ai-lab/colab/)**: โค้ดสำหรับรันเซิร์ฟเวอร์ AI บน Google Colab (Tesla T4 GPU ฟรี 15GB VRAM) พร้อมเปิด Cloudflare Tunnel
  * **[`client/`](file:///C:/Users/PC/Documents/New%20project/security-ai-lab/client/)**: สคริปต์ไคลเอนต์น้ำหนักเบา (Zero-Dependency) สำหรับสั่งการจาก Kali Linux, Arch Linux, และ Windows
  * **[`guides/`](file:///C:/Users/PC/Documents/New%20project/security-ai-lab/guides/)**: คู่มือสถาปัตยกรรม, ข้อจำกัดของ Colab, วิธีการเชื่อมต่อ และตัวอย่างโจทย์สำหรับฝึกฝนในแล็บ

---

## จุดเด่นของโปรเจกต์นี้

1. **ไม่กินทรัพยากรเครื่องตัวเอง:** ไม่ต้องกังวลว่าเครื่องจะรันโมเดลไม่ไหว เพราะยกภาระการประมวลผลทั้งหมดไปไว้บน Cloud GPU ฟรี
2. **โมเดลไม่เซ็นเซอร์ (Abliterated):** ปลดบล็อกเวกเตอร์การปฏิเสธออก ทำให้ศึกษาเทคนิค Reverse Engineering, Shellcode, Memory Corruption, และสคริปต์ความปลอดภัยเพื่อการศึกษาได้อย่างไม่ติดขัด
3. **ใช้งานง่าย:** รัน Colab 1-Click แล้วใช้คำสั่งเดียวใน Kali / Arch ยิงคำถามได้ทันที

อ่านรายละเอียดฉบับเต็มได้ที่ **[`security-ai-lab/README.md`](file:///C:/Users/PC/Documents/New%20project/security-ai-lab/README.md)**
