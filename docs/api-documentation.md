# API Documentation

## ภาพรวม

API ของระบบ AI Property Consultant ถูกออกแบบมาเพื่อให้บริการข้อมูลและฟังก์ชันการทำงานต่างๆ ผ่าน RESTful endpoints

## Endpoints

### 1. GET /api/styles
ดึงข้อมูลรูปแบบการสนทนาที่มีในระบบ

**Request:**
```http
GET /api/styles
```

**Response:**
```json
{
    "styles": [
        {
            "id": "formal",
            "name": "ทางการ",
            "description": "ใช้ภาษาทางการ โครงสร้างประโยคเป็นทางการ"
        },
        {
            "id": "casual",
            "name": "ไม่เป็นทางการ",
            "description": "ใช้ภาษาพูดทั่วไป โครงสร้างประโยคไม่เป็นทางการ"
        },
        {
            "id": "friendly",
            "name": "เป็นมิตร",
            "description": "ใช้ภาษาที่เป็นมิตร เข้าใจง่าย"
        },
        {
            "id": "professional",
            "name": "มืออาชีพ",
            "description": "ใช้ภาษามืออาชีพ มีคำศัพท์เฉพาะ"
        }
    ]
}
```

### 2. POST /api/save_history
บันทึกประวัติการสนทนา

**Request:**
```http
POST /api/save_history
Content-Type: application/json

{
    "session_id": "123456",
    "messages": [
        {
            "role": "user",
            "content": "ต้องการคอนโดใกล้รถไฟฟ้าสีลม",
            "timestamp": "2024-03-20T10:00:00Z"
        },
        {
            "role": "assistant",
            "content": "มีคอนโดหลายแห่งใกล้รถไฟฟ้าสีลม...",
            "timestamp": "2024-03-20T10:00:01Z"
        }
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "บันทึกประวัติการสนทนาเรียบร้อยแล้ว"
}
```

### 3. GET /api/properties
ดึงข้อมูลอสังหาริมทรัพย์ทั้งหมด

**Request:**
```http
GET /api/properties
```

**Response:**
```json
{
    "properties": [
        {
            "_id": "507f1f77bcf86cd799439011",
            "ประเภท": "คอนโด",
            "ชื่อ": "คอนโดสุขุมวิท",
            "ตำแหน่ง": "สุขุมวิท",
            "ราคา": 5000000,
            "รายละเอียด": "คอนโดหรู ใกล้รถไฟฟ้า"
        },
        {
            "_id": "507f1f77bcf86cd799439012",
            "ประเภท": "บ้าน",
            "ชื่อ": "บ้านเดี่ยวสุขุมวิท",
            "ตำแหน่ง": "สุขุมวิท",
            "ราคา": 10000000,
            "รายละเอียด": "บ้านเดี่ยวสไตล์โมเดิร์น"
        }
    ]
}
```

### 4. POST /api/analyze
วิเคราะห์ความสนใจของผู้ใช้

**Request:**
```http
POST /api/analyze
Content-Type: application/json

{
    "query": "ต้องการคอนโดใกล้รถไฟฟ้าสีลม",
    "consultation_style": "formal",
    "language": "thai"
}
```

**Response:**
```json
{
    "interests": [
        {
            "property": {
                "_id": "507f1f77bcf86cd799439011",
                "ประเภท": "คอนโด",
                "ชื่อ": "คอนโดสุขุมวิท",
                "ตำแหน่ง": "สุขุมวิท",
                "ราคา": 5000000,
                "รายละเอียด": "คอนโดหรู ใกล้รถไฟฟ้า"
            },
            "score": 0.95
        }
    ],
    "detected_property_type": "คอนโด",
    "detected_location": "สีลม"
}
```

## การจัดการข้อผิดพลาด

### รหัสข้อผิดพลาด
- 400: Bad Request - ข้อมูลที่ส่งมาไม่ถูกต้อง
- 401: Unauthorized - ไม่มีสิทธิ์เข้าถึง
- 404: Not Found - ไม่พบข้อมูล
- 500: Internal Server Error - ข้อผิดพลาดภายในเซิร์ฟเวอร์

### ตัวอย่างข้อผิดพลาด
```json
{
    "error": {
        "code": 400,
        "message": "ข้อมูลที่ส่งมาไม่ถูกต้อง",
        "details": "กรุณาตรวจสอบข้อมูลที่ส่งมา"
    }
}
```

## การบำรุงรักษา

### การอัปเดต
- เพิ่ม endpoints ใหม่
- ปรับปรุง endpoints ที่มีอยู่
- เพิ่มฟีเจอร์ใหม่

### การตรวจสอบ
- ตรวจสอบประสิทธิภาพ
- ตรวจสอบความปลอดภัย
- ตรวจสอบความถูกต้องของข้อมูล

### การสำรองข้อมูล
- สำรองข้อมูล API
- มีแผนกู้คืนเมื่อเกิดปัญหา
- ทดสอบระบบเป็นประจำ 