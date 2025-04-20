# โครงสร้างและ Logic ของ ChatAI

## 1. โครงสร้างระบบ

### 1.1 Frontend
- **React + TypeScript**
  - ใช้ Vite เป็น build tool
  - Tailwind CSS สำหรับ UI
  - ESLint และ Prettier สำหรับ code quality

### 1.2 Backend
- **Python + FastAPI**
  - MongoDB เป็นฐานข้อมูล
  - Sentence Transformers สำหรับ AI
  - Hugging Face Transformers

## 2. โครงสร้างโค้ด

### 2.1 Frontend Structure
```
src/
├── components/     # React components
├── pages/         # หน้าเว็บต่างๆ
├── services/      # API services
├── utils/         # utility functions
└── types/         # TypeScript types
```

### 2.2 Backend Structure
```
src/backend/
├── api/           # API endpoints
├── models/        # database models
├── services/      # business logic
├── utils/         # utility functions
└── config/        # configuration files
```

## 3. Logic การทำงาน

### 3.1 การประมวลผลข้อความ
1. รับข้อความจากผู้ใช้
2. แปลงเป็นเวกเตอร์
3. ค้นหาข้อมูลที่เกี่ยวข้อง
4. สร้างคำตอบ
5. ส่งกลับไปยังผู้ใช้

### 3.2 การวิเคราะห์ผู้ใช้
1. เก็บข้อมูลการใช้งาน
2. วิเคราะห์พฤติกรรม
3. สร้างโปรไฟล์
4. ปรับแต่งการแนะนำ

### 3.3 การจัดการข้อมูล
1. เก็บข้อมูลใน MongoDB
2. อัพเดทข้อมูลอัตโนมัติ
3. ทำความสะอาดข้อมูล
4. สำรองข้อมูล

## 4. การเชื่อมต่อระบบ

### 4.1 Frontend-Backend
- REST API
- WebSocket สำหรับ real-time
- JWT สำหรับ authentication

### 4.2 Backend-Database
- MongoDB connection
- Connection pooling
- Error handling

## 5. ความปลอดภัย

### 5.1 การป้องกันข้อมูล
- การเข้ารหัสข้อมูล
- การตรวจสอบสิทธิ์
- การป้องกัน SQL Injection

### 5.2 การจัดการ Session
- Session management
- Token-based authentication
- Rate limiting 