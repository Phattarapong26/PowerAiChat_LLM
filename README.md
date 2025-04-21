# AI Property Consultant System

ระบบที่ปรึกษาอสังหาริมทรัพย์อัจฉริยะ ที่ใช้เทคโนโลยี AI ในการให้คำแนะนำเกี่ยวกับอสังหาริมทรัพย์

## ภาพรวมระบบ

ระบบนี้เป็นแพลตฟอร์มที่ใช้ AI ในการให้คำแนะนำเกี่ยวกับอสังหาริมทรัพย์ โดยมีฟีเจอร์หลักดังนี้:

- การสนทนากับ AI ที่ปรึกษา
- การค้นหาอสังหาริมทรัพย์ด้วย Vector Search
- การวิเคราะห์ความสนใจของผู้ใช้
- การจัดการข้อมูลอสังหาริมทรัพย์
- การรองรับหลายภาษา (ไทย/อังกฤษ)
- การปรับแต่งสไตล์การให้คำปรึกษา

## เอกสารระบบ

- [ภาพรวมสถาปัตยกรรม](docs/architecture.md)
- [การทำงานของ Vector Search](docs/vector-search.md)
- [การวิเคราะห์ผู้ใช้](docs/user-analysis.md)
- [การออกแบบการตอบสนอง](docs/response-design.md)
- [API Documentation](docs/api.md)
- [Prompt Engineering](docs/prompt-engineering.md)
- [การจัดการข้อมูล](docs/data-management.md)
- [Flow Diagram](docs/flow-diagram.md)

## การติดตั้งและใช้งาน

1. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

2. ตั้งค่า environment variables:
```bash
cp .env.example .env
```

3. เริ่มต้นระบบ:
```bash
python src/backend/run.py
```

## ข้อกำหนดระบบ

- Python 3.8+
- MongoDB
- Node.js 16+
- React 18+

## การพัฒนา

- Frontend: React + TypeScript
- Backend: FastAPI + Python
- Database: MongoDB
- Vector Search: Sentence Transformers
- Authentication: JWT

## ผู้พัฒนา

- [ชื่อทีม/บริษัท]
- [ติดต่อ]
