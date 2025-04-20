# คู่มือระบบ ChatAI 🏠

## สารบัญ
1. [ภาพรวมของระบบ](#1-ภาพรวมของระบบ)
2. [สถาปัตยกรรมระบบ](#2-สถาปัตยกรรมระบบ)
3. [การติดตั้งและตั้งค่าระบบ](#3-การติดตั้งและตั้งค่าระบบ)
4. [การพัฒนาและทดสอบ](#4-การพัฒนาและทดสอบ)
5. [การใช้งานระบบ](#5-การใช้งานระบบ)
6. [การบำรุงรักษาและแก้ไขปัญหา](#6-การบำรุงรักษาและแก้ไขปัญหา)
7. [ความปลอดภัย](#7-ความปลอดภัย)
8. [การอัพเกรดและขยายระบบ](#8-การอัพเกรดและขยายระบบ)

## 1. ภาพรวมของระบบ

### 1.1 จุดประสงค์ของระบบ
ระบบ ChatAI เป็นแพลตฟอร์มให้คำปรึกษาด้านอสังหาริมทรัพย์ที่ใช้เทคโนโลยี AI ในการวิเคราะห์และตอบคำถามของผู้ใช้ โดยมีจุดประสงค์หลักดังนี้:
- ให้คำปรึกษาด้านอสังหาริมทรัพย์แบบอัตโนมัติ
- ค้นหาและแนะนำอสังหาริมทรัพย์ที่เหมาะสม
- วิเคราะห์ความต้องการของผู้ใช้
- รองรับการใช้งานภาษาไทยและอังกฤษ

### 1.2 ฟีเจอร์หลัก
1. การให้คำปรึกษาด้านอสังหาริมทรัพย์
2. การค้นหาอสังหาริมทรัพย์
3. การวิเคราะห์ผู้ใช้
4. การแปลภาษา
5. การจัดการข้อมูลอสังหาริมทรัพย์

## 2. สถาปัตยกรรมระบบ

### 2.1 โครงสร้างระบบ
ระบบแบ่งเป็น 2 ส่วนหลัก:
1. Frontend (React + TypeScript)
   - `/src/components`: React components
   - `/src/pages`: หน้าเว็บต่างๆ
   - `/src/context`: React context
   - `/src/hooks`: Custom React hooks
   - `/src/types`: TypeScript type definitions

2. Backend (Python + FastAPI)
   - `/src/backend/main.py`: FastAPI application
   - `/src/backend/config.py`: การตั้งค่าระบบ
   - `/src/backend/vector_store.py`: การจัดการ vector search
   - `/src/backend/language_models.py`: การจัดการ language models
   - `/src/backend/mongodb_manager.py`: การจัดการฐานข้อมูล
   - `/src/backend/user_analyzer.py`: การวิเคราะห์ผู้ใช้

### 2.2 เทคโนโลยีที่ใช้
1. Frontend:
   - React 18
   - TypeScript
   - Vite
   - TailwindCSS

2. Backend:
   - Python 3.9+
   - FastAPI
   - MongoDB
   - Sentence Transformers
   - Hugging Face Transformers

### 2.3 การเชื่อมต่อระหว่างระบบ
1. API Endpoints:
   - `/api/chat`: สำหรับการสนทนา
   - `/api/upload`: สำหรับอัพโหลดข้อมูล
   - `/api/styles`: สำหรับดึงสไตล์การให้คำปรึกษา

2. การเชื่อมต่อฐานข้อมูล:
   - MongoDB สำหรับเก็บข้อมูลอสังหาริมทรัพย์
   - MongoDB สำหรับเก็บข้อมูลผู้ใช้และ session

## 3. การติดตั้งและตั้งค่าระบบ

### 3.1 ความต้องการของระบบ
1. Frontend:
   ```bash
   Node.js >= 16
   npm >= 8
   ```

2. Backend:
   ```bash
   Python >= 3.9
   pip >= 21
   MongoDB >= 4.4
   ```

### 3.2 ขั้นตอนการติดตั้ง
1. ติดตั้ง Frontend:
   ```bash
   cd src
   npm install
   npm run dev
   ```

2. ติดตั้ง Backend:
   ```bash
   cd src/backend
   pip install -r requirements.txt
   python run.py
   ```

### 3.3 การตั้งค่าระบบ
1. ไฟล์ config.py:
   ```python
   MONGODB_URL = "mongodb://localhost:27017/AI"
   MONGODB_DB = "AI"
   MODEL_CONFIG = {
       'language_model': 'google/flan-t5-base',
       'embedding_model': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
       'translation_model': 'Helsinki-NLP/opus-mt-th-en'
   }
   ```

2. ตัวแปรสภาพแวดล้อม:
   ```bash
   MONGODB_URL=mongodb://localhost:27017/AI
   MONGODB_DB=AI
   API_KEY=your_api_key
   ```

## 4. การพัฒนาและทดสอบ

### 4.1 การพัฒนา Frontend
1. โครงสร้าง Component:
   ```typescript
   // src/components/Chat.tsx
   interface ChatProps {
     messages: Message[];
     onSend: (message: string) => void;
   }
   ```

2. การจัดการ State:
   ```typescript
   // src/context/ChatContext.tsx
   interface ChatContextType {
     messages: Message[];
     sendMessage: (message: string) => void;
   }
   ```

### 4.2 การพัฒนา Backend
1. การเพิ่ม API Endpoint:
   ```python
   @app.post("/api/chat")
   async def chat(query: PropertyQuery):
       # Implementation
   ```

2. การเพิ่ม Model:
   ```python
   class PropertyQuery(BaseModel):
       query: str
       consultation_style: str
       session_id: Optional[str]
   ```

### 4.3 การทดสอบ
1. Frontend Tests:
   ```bash
   npm run test
   ```

2. Backend Tests:
   ```bash
   python -m pytest tests/
   ```

## 5. การใช้งานระบบ

### 5.1 การใช้งาน Frontend
1. การเริ่มต้นสนทนา:
   - เปิดหน้าเว็บ
   - เลือกสไตล์การให้คำปรึกษา
   - พิมพ์คำถาม

2. การอัพโหลดข้อมูล:
   - ไปที่หน้าอัพโหลด
   - เลือกไฟล์ CSV หรือ Excel
   - กดอัพโหลด

### 5.2 การใช้งาน Backend
1. การเรียกใช้ API:
   ```bash
   curl -X POST "http://localhost:8000/api/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "ต้องการซื้อคอนโดใกล้ BTS"}'
   ```

2. การจัดการฐานข้อมูล:
   ```python
   mongodb_manager = MongoDBManager()
   properties = mongodb_manager.get_properties()
   ```

## 6. การบำรุงรักษาและแก้ไขปัญหา

### 6.1 การตรวจสอบระบบ
1. Frontend Logs:
   ```bash
   npm run dev
   ```

2. Backend Logs:
   ```bash
   python run.py
   ```

### 6.2 การแก้ไขปัญหาทั่วไป
1. Frontend Issues:
   - ตรวจสอบ Console ใน Developer Tools
   - ตรวจสอบ Network Requests
   - ตรวจสอบ React DevTools

2. Backend Issues:
   - ตรวจสอบ Logs
   - ตรวจสอบ MongoDB Connection
   - ตรวจสอบ API Responses

## 7. ความปลอดภัย

### 7.1 การป้องกันข้อมูล
1. API Authentication:
   ```python
   API_KEY_NAME = "X-API-Key"
   API_KEY = os.getenv("API_KEY")
   ```

2. MongoDB Security:
   - ใช้ Authentication
   - จำกัดการเข้าถึง
   - เข้ารหัสข้อมูล

### 7.2 การจัดการ Session
1. Session Management:
   ```python
   def create_session(session_id: str):
       session_data = {
           "session_id": session_id,
           "created_at": datetime.now(),
           "messages": []
       }
   ```

2. Session Cleanup:
   ```python
   def cleanup_old_sessions():
       # Remove sessions older than 24 hours
   ```

## 8. การอัพเกรดและขยายระบบ

### 8.1 การอัพเกรด Frontend
1. อัพเดท Dependencies:
   ```bash
   npm update
   ```

2. อัพเดท React Components:
   ```bash
   npm run build
   ```

### 8.2 การอัพเกรด Backend
1. อัพเดท Dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. อัพเดท Models:
   ```python
   # Update model versions in config.py
   MODEL_CONFIG = {
       'language_model': 'new_model_version',
       'embedding_model': 'new_model_version'
   }
   ```

### 8.3 การขยายระบบ
1. เพิ่ม Language Models:
   - เพิ่มโมเดลใหม่ใน config.py
   - อัพเดท language_models.py

2. เพิ่ม Features:
   - เพิ่ม API endpoints
   - อัพเดท frontend components
   - เพิ่ม database collections 