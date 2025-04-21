# 🏠 AI Property Consultant

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Node](https="img.shields.io/badge/node-16+-green.svg)

ระบบที่ปรึกษาอสังหาริมทรัพย์อัจฉริยะ ที่ให้บริการทั้งภาษาไทยและอังกฤษ

[เริ่มต้นใช้งาน](docs/user-guide.md) • [คุณสมบัติ](docs/detailsystem.md) • [เอกสาร](docs/index.md) • [ติดต่อเรา](#support)

</div>

## 📋 ภาพรวม
AI Property Consultant เป็นระบบ chatbot อัจฉริยะที่ออกแบบมาเพื่อให้บริการที่ปรึกษาด้านอสังหาริมทรัพย์ทั้งภาษาไทยและอังกฤษ ระบบใช้เทคโนโลยีการประมวลผลภาษาธรรมชาติขั้นสูงในการทำความเข้าใจคำถามของผู้ใช้และให้ข้อมูลอสังหาริมทรัพย์ที่เกี่ยวข้อง พร้อมทั้งสามารถปรับรูปแบบการสนทนาได้ตามต้องการ

## ✨ คุณสมบัติ
- 🌐 รองรับ 2 ภาษา (ไทย/อังกฤษ)
- 🎭 รูปแบบการให้คำปรึกษาหลากหลาย (ทางการ, สบายๆ, เป็นมิตร, มืออาชีพ)
- 🔍 ค้นหาและแนะนำอสังหาริมทรัพย์
- 👤 ระบบยืนยันตัวตนและจัดการเซสชัน
- 📝 บันทึกประวัติการสนทนา
- 📤 จัดการข้อมูลอสังหาริมทรัพย์ผ่านการอัปโหลดไฟล์
- 💾 เชื่อมต่อกับ MongoDB สำหรับจัดเก็บข้อมูล
- 🔎 ค้นหาเชิงความหมายด้วย Vector
- 💝 สร้างคำตอบที่เข้าใจความรู้สึก

## 🛠 เทคโนโลยีที่ใช้
- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI + Python
- **ฐานข้อมูล:** MongoDB
- **UI Framework:** Tailwind CSS
- **การจัดการ State:** React Context
- **การเชื่อมต่อ API:** Axios

## ⚙️ ความต้องการของระบบ
- Node.js 16+
- Python 3.8+
- MongoDB 4.4+
- npm หรือ yarn

## 🚀 การติดตั้ง

### การติดตั้ง Backend
1. เข้าไปที่โฟลเดอร์ backend:
```bash
cd src/backend
```

2. สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # สำหรับ Unix
venv\Scripts\activate     # สำหรับ Windows
```

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

4. ตั้งค่า MongoDB:
- สร้างไฟล์ `.env` ในโฟลเดอร์ backend
- เพิ่ม connection string:
```
MONGODB_URL=mongodb://localhost:27017/AI
MONGODB_DB=AI
```

### การติดตั้ง Frontend
1. ติดตั้ง dependencies:
```bash
npm install
# หรือ
yarn install
```

2. ตั้งค่าสภาพแวดล้อม:
สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:
```
VITE_API_URL=http://localhost:8000
```

## 🏃‍♂️ การใช้งาน

### เริ่ม Backend Server
```bash
cd src/backend
uvicorn main:app --reload
```

### เริ่ม Frontend Development Server
```bash
npm run dev
# หรือ
yarn dev
```

## 📡 API Endpoints

### Chat API
- `POST /api/chat`
  - ประมวลผลคำถามผู้ใช้และส่งคืนคำแนะนำเกี่ยวกับอสังหาริมทรัพย์
  - รองรับการเลือกรูปแบบการสนทนาและภาษา

### การจัดการผู้ใช้
- `POST /api/register`
  - ลงทะเบียนผู้ใช้
- `POST /api/login`
  - ยืนยันตัวตนผู้ใช้

### การจัดการข้อมูล
- `POST /api/upload`
  - อัปโหลดข้อมูลอสังหาริมทรัพย์ผ่าน CSV/Excel
- `GET /api/styles`
  - ดึงรูปแบบการให้คำปรึกษาที่มีอยู่

### ประวัติการสนทนา
- `POST /api/save_history`
  - บันทึกประวัติการสนทนา
- `GET /api/chat` (with get_history=true)
  - ดึงประวัติการสนทนา

## 📁 โครงสร้างโปรเจค
```
.
├── src/
│   ├── backend/
│   │   ├── main.py              # FastAPI application
│   │   ├── mongodb_manager.py   # Database operations
│   │   ├── language_models.py   # Response generation
│   │   ├── vector_store.py      # Semantic search
│   │   ├── config.py           # Configuration
│   │   └── requirements.txt    # Python dependencies
│   ├── frontend/
│   │   ├── api.ts             # API integration
│   │   └── components/        # React components
│   └── types/                 # TypeScript types
├── package.json
└── README.md
```

## 🔧 องค์ประกอบหลัก

### Backend Components
1. **FastAPI Application** (`main.py`)
   - API endpoints และการจัดการคำขอ
   - การประมวลผลการสนทนาและการสร้างคำตอบ
   - การจัดการการอัปโหลดไฟล์

2. **MongoDB Manager** (`mongodb_manager.py`)
   - การดำเนินการกับฐานข้อมูล
   - การจัดการเซสชัน
   - การจัดการข้อมูลผู้ใช้

3. **Language Models** (`language_models.py`)
   - การสร้างคำตอบ
   - รองรับหลายภาษา
   - การจัดการรูปแบบการให้คำปรึกษา

4. **Vector Store** (`vector_store.py`)
   - การค้นหาเชิงความหมาย
   - การจับคู่อสังหาริมทรัพย์

### Frontend Components
1. **API Integration** (`api.ts`)
   - การสื่อสารกับ Backend
   - การจัดการคำขอ/คำตอบ

2. **React Components**
   - หน้าต่างการสนทนา
   - การแสดงผลอสังหาริมทรัพย์
   - การจัดการผู้ใช้
   - การอัปโหลดไฟล์

## 🤝 การมีส่วนร่วม
1. Fork โปรเจค
2. สร้าง feature branch
3. Commit การเปลี่ยนแปลง
4. Push ไปยัง branch
5. สร้าง Pull Request

## 📄 ลิขสิทธิ์
โปรเจคนี้ได้รับลิขสิทธิ์ภายใต้ MIT License

## 📞 การสนับสนุน
สำหรับการสนับสนุน กรุณาเปิด issue ใน repository หรือติดต่อทีมพัฒนา

---

<div align="center">
Made with ❤️ by AI Property Consultant Team
</div>
