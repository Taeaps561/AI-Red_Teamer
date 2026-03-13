# AI-Red Teamer: Local AI-Powered Security Scanner

ระบบความมั่นคงปลอดภัยอัจฉริยะที่ใช้ **Local LLM (Ollama)** ในการวิเคราะห์โค้ดและจำลองการโจมตีอัตโนมัติ (Automated Red Teaming) เพื่อตรวจหาช่องโหว่ OWASP Top 10 ก่อนการ Deploy

## 🚀 คุณสมบัติเด่น (Features)
- **AI-Driven Analysis**: ใช้ Ollama (llama3.2) วิเคราะห์โค้ดแบบ Privacy-First (ไม่ต้องส่งคัดไป Cloud)
- **Automated Verification**: ยืนยันช่องโหว่ด้วยการลองโจมตีจริง (Exploit Simulation) ผ่าน Pytest
- **CI/CD Integration**: รองรับ GitHub Actions เพื่อหยุด Pipeline ทันทีที่พบช่องโหว่ระดับ High
- **Vulnerability Reporting**: สร้างรายงาน `security_report.md` สรุปผลและแนวทางการแก้ไข

## 🛠 โครงสร้างระบบ (Architecture)
ระบบประกอบด้วย 4 ส่วนหลัก:
1. **Scanner Engine**: สแกนหาไฟล์ที่แก้ไขและส่งไปที่ Local AI
2. **Attack Verifier**: นำ Payload จาก AI ไปลองยิงใส่ Mock Server
3. **Mock Engine**: เซิร์ฟเวอร์จำลองที่มีช่องโหว่เพื่อใช้ทดสอบ
4. **Orchestrator**: ตัวควบคุมการทำงานทั้งหมดและส่งค่า Exit Code ให้ CI/CD

## 📦 วิธีการติดตั้ง (Quick Start)

1. **ติดตั้ง Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **เปิดระบบ Ollama**:
   - ติดตั้ง [Ollama](https://ollama.com/)
   - รันโมเดล: `ollama run llama3.2`

3. **รันการสแกนแบบ Local**:
   ```bash
   python main_redteam.py
   ```

4. **รันการทดสอบระบบ (Full Test Suite)**:
   ```bash
   python -m pytest tests/test_redteam_logic.py
   ```

## 🛡 การตั้งค่าใน GitHub
หากต้องการนำไปใช้ใน GitHub Actions ให้เพิ่ม Secrets ดังนี้:
- `GITHUB_TOKEN`: สำหรับการตรวจสอบสิทธิ์
- `OPENAI_API_KEY`: (ตัวเลือก) หากต้องการเปลี่ยนไปใช้ GPT-4o แทน Ollama (ปรับใน `scanner_engine.py`)

## 📄 ใบอนุญาต (License)
MIT License
