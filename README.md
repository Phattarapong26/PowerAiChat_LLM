# ChatAI - แอปพลิเคชันแชทอัจฉริยะ

แอปพลิเคชันแชทอัจฉริยะที่พัฒนาด้วย React, TypeScript และ Vite

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
