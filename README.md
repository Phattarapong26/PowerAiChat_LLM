# ChatAI - แอปพลิเคชันแชทอัจฉริยะ

แอปพลิเคชันแชทอัจฉริยะที่พัฒนาด้วย React, TypeScript และ Vite สำหรับให้คำปรึกษาด้านอสังหาริมทรัพย์

## 🚀 คุณสมบัติหลัก

- 💬 การสนทนาอัจฉริยะด้วย AI
- 🎨 หน้าต่างที่ทันสมัยด้วย Tailwind CSS
- 📱 รองรับการใช้งานบนทุกอุปกรณ์
- ⚡ ประสิทธิภาพสูงด้วย Vite
- 🔄 รองรับการแปลภาษาไทย-อังกฤษ
- 📊 ระบบวิเคราะห์ผู้ใช้
- 🔍 ค้นหาอสังหาริมทรัพย์แบบ Vector Search

## 📚 เอกสารประกอบ

- [คู่มือการใช้งาน](./docs/user-guide.md)
- [กระบวนการทำงาน](./docs/workflow.md)
- [โครงสร้างและ Logic](./docs/architecture.md)
- [รายละเอียดระบบ Backend](./docs/backend-explained.md)
- [คู่มือการพัฒนา](./docs/detailsystem.md)
- [อธิบายโค้ด Backend](./docs/backend-code-explained.md)

## 🛠️ การติดตั้ง

### Frontend
```bash
# ติดตั้ง dependencies
npm install

# รันในโหมด development
npm run dev

# สร้างไฟล์สำหรับ production
npm run build
```

### Backend
```bash
# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ติดตั้ง dependencies
cd src/backend
pip install -r requirements.txt

# รัน server
python run.py
```

### การตั้งค่าตัวแปรสภาพแวดล้อม
สร้างไฟล์ `.env` ในโฟลเดอร์ `src/backend`:
```bash
MONGODB_URL=mongodb://localhost:27017/AI
MONGODB_DB=AI
API_KEY=your_api_key
MODEL_CONFIG_PATH=config.json
```

## 🔧 เทคโนโลยีที่ใช้

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- ESLint
- Prettier

### Backend
- Python 3.9+
- FastAPI
- MongoDB
- Sentence Transformers
- Hugging Face Transformers

## 📊 ระบบวิเคราะห์ผู้ใช้

ระบบวิเคราะห์ผู้ใช้ของ ChatAI ทำงานดังนี้:

1. **การเก็บข้อมูลผู้ใช้**
   - เก็บประวัติการสนทนาใน MongoDB
   - วิเคราะห์ความสนใจจากคำถาม
   - ดูประวัติการค้นหา
   - เก็บข้อมูลการใช้งาน เช่น เวลาที่ใช้งาน, ความถี่ในการใช้งาน, ประเภทคำถามที่สนใจ

2. **การวิเคราะห์พฤติกรรม**
   - วิเคราะห์คำสำคัญจากประวัติการค้นหา
   - แยกประเภทความสนใจ เช่น สถานที่, ประเภทอสังหาริมทรัพย์, ช่วงราคา, สิ่งอำนวยความสะดวก
   - สร้างโปรไฟล์ผู้ใช้ที่แสดงความสนใจหลัก

3. **การแนะนำอสังหาริมทรัพย์**
   - แนะนำอสังหาริมทรัพย์ที่เกี่ยวข้องกับความสนใจของผู้ใช้
   - ใช้ข้อมูลจากการวิเคราะห์พฤติกรรม
   - แสดงข้อมูลที่เกี่ยวข้อง เช่น ราคา สถานที่ตั้ง
   - ปรับแต่งการแนะนำตามพฤติกรรมผู้ใช้

## 🤖 การประมวลผล AI

### การแปลงข้อความเป็นเวกเตอร์
1. **กระบวนการแปลง**
   - ใช้โมเดล `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
   - แปลงข้อความภาษาไทยและอังกฤษเป็นเวกเตอร์ 384 มิติ
   - เก็บเวกเตอร์ใน MongoDB สำหรับการค้นหาอย่างรวดเร็ว

2. **การใช้งานเวกเตอร์**
   - ใช้สำหรับค้นหาอสังหาริมทรัพย์ที่เกี่ยวข้องกับคำถาม
   - คำนวณความคล้ายคลึงระหว่างเวกเตอร์คำถามและเวกเตอร์อสังหาริมทรัพย์
   - ใช้เกณฑ์ความคล้ายคลึง (Similarity Threshold) ที่ 0.1
   - แสดงผลลัพธ์สูงสุด 5 รายการ

### ระบบค้นหาแบบ Vector Search
1. **การทำงานของ Vector Search**
   - รับคำถามจากผู้ใช้
   - แปลงคำถามเป็นเวกเตอร์
   - ค้นหาเวกเตอร์ที่มีความคล้ายคลึงสูงในฐานข้อมูล
   - คืนค่าอสังหาริมทรัพย์ที่เกี่ยวข้อง

2. **การปรับแต่งการค้นหา**
   - ปรับเกณฑ์ความคล้ายคลึงตามความต้องการ
   - เพิ่มน้ำหนักให้กับคำสำคัญบางคำ
   - รองรับการค้นหาแบบ Fuzzy Match
   - จำกัดจำนวนผลลัพธ์ที่แสดง

## 🔌 การจัดการ API

### Endpoints หลัก
1. **/api/chat**
   - รับข้อความจากผู้ใช้
   - ประมวลผลด้วย AI
   - ส่งคำตอบกลับไปยังผู้ใช้
   - ตัวอย่างการใช้งาน:
     ```json
     {
       "query": "ต้องการซื้อคอนโดใกล้ BTS",
       "consultation_style": "formal",
       "session_id": "optional-session-id"
     }
     ```

2. **/api/upload**
   - อัพโหลดข้อมูลอสังหาริมทรัพย์
   - รองรับไฟล์ Excel และ CSV
   - ตรวจสอบความถูกต้องของข้อมูล
   - ตัวอย่างการใช้งาน:
     ```
     POST /api/upload
     Content-Type: multipart/form-data
     
     file: [ไฟล์ Excel หรือ CSV]
     consultation_style: formal
     ```

3. **/api/styles**
   - ดึงรายการสไตล์การให้คำปรึกษา
   - ตัวอย่างการใช้งาน:
     ```
     GET /api/styles
     ```

### ขั้นตอนการประมวลผลข้อความ
1. **การรับข้อความ**
   - รับข้อความจาก API endpoint
   - ตรวจสอบความถูกต้องของข้อมูล
   - ดึง session_id หรือสร้าง session ใหม่

2. **การประมวลผล**
   - แปลงข้อความเป็นเวกเตอร์
   - ค้นหาอสังหาริมทรัพย์ที่เกี่ยวข้อง
   - สร้างคำตอบตามสไตล์ที่เลือก
   - บันทึกประวัติการสนทนา

3. **การส่งคำตอบ**
   - ส่งคำตอบกลับไปยังผู้ใช้
   - พร้อมข้อมูลอสังหาริมทรัพย์ที่เกี่ยวข้อง
   - ตัวอย่างคำตอบ:
     ```json
     {
       "response": "สำหรับคำถามเกี่ยวกับ 'ต้องการซื้อคอนโดใกล้ BTS' ทางเรามีข้อมูลอสังหาริมทรัพย์ที่น่าสนใจดังนี้...",
       "session_id": "session_12345abcde",
       "properties": [...]
     }
     ```

## 📝 License

MIT License - ดูรายละเอียดเพิ่มเติมได้ที่ [LICENSE](./LICENSE)

## 🤝 การมีส่วนร่วม

1. Fork โปรเจค
2. สร้าง branch ใหม่ (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

## 📞 การติดต่อ

- Email: phattarapong.phe@spumail.net
- Documentation: https://docs.chatai.com
