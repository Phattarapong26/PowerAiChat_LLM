# 📚 API Documentation

## 1. ข้อมูลทั่วไป (General Information)

### Base URL
```
http://localhost:8000
```

### Headers
```
Content-Type: application/json
X-API-Key: your_api_key
```

## 2. Authentication

### ลงทะเบียนผู้ใช้ (Register User)
```http
POST /api/register
```

**Request Body:**
```json
{
    "name": "ชื่อผู้ใช้",
    "email": "email@example.com",
    "password": "รหัสผ่าน"
}
```

**Response:**
```json
{
    "id": "user_id",
    "name": "ชื่อผู้ใช้",
    "email": "email@example.com",
    "created_at": "2024-04-21T08:00:00Z"
}
```

### เข้าสู่ระบบ (Login)
```http
POST /api/login
```

**Request Body:**
```json
{
    "email": "email@example.com",
    "password": "รหัสผ่าน"
}
```

**Response:**
```json
{
    "id": "user_id",
    "name": "ชื่อผู้ใช้",
    "email": "email@example.com",
    "session_id": "session_id"
}
```

## 3. การสนทนา (Chat)

### ส่งข้อความ (Send Message)
```http
POST /api/chat
```

**Request Body:**
```json
{
    "query": "ข้อความที่ต้องการถาม",
    "consultation_style": "formal",
    "session_id": "session_id",
    "chat_room_id": "chat_room_id",
    "save_message": true,
    "timestamp": 1711008000000,
    "get_history": false,
    "language": "thai",
    "user_id": "user_id"
}
```

**Response:**
```json
{
    "response": "คำตอบจาก AI",
    "session_id": "session_id",
    "chat_room_id": "chat_room_id",
    "properties": [
        {
            "id": "property_id",
            "ประเภท": "ประเภทอสังหาริมทรัพย์",
            "โครงการ": "ชื่อโครงการ",
            "ราคา": "ราคา",
            "รูปแบบ": "รูปแบบ",
            "ตำแหน่ง": "ตำแหน่ง",
            "สถานศึกษา": "สถานศึกษาใกล้เคียง",
            "สถานีรถไฟฟ้า": "สถานีรถไฟฟ้าใกล้เคียง",
            "ห้างสรรพสินค้า": "ห้างสรรพสินค้าใกล้เคียง"
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "ข้อความของผู้ใช้",
            "timestamp": 1711008000000
        },
        {
            "role": "assistant",
            "content": "คำตอบจาก AI",
            "timestamp": 1711008001000,
            "properties": []
        }
    ]
}
```

## 4. การจัดการข้อมูล (Data Management)

### อัปโหลดข้อมูล (Upload Data)
```http
POST /api/upload
```

**Request Body:**
```multipart/form-data
file: file.csv
```

**Response:**
```json
{
    "message": "อัปโหลดสำเร็จ",
    "file_id": "file_id",
    "total_records": 100
}
```

### ดึงข้อมูลอสังหาริมทรัพย์ (Get Properties)
```http
GET /api/properties
```

**Query Parameters:**
```
type: ประเภทอสังหาริมทรัพย์
price_min: ราคาต่ำสุด
price_max: ราคาสูงสุด
location: ตำแหน่ง
```

**Response:**
```json
{
    "properties": [
        {
            "id": "property_id",
            "ประเภท": "ประเภทอสังหาริมทรัพย์",
            "โครงการ": "ชื่อโครงการ",
            "ราคา": "ราคา",
            "รูปแบบ": "รูปแบบ",
            "ตำแหน่ง": "ตำแหน่ง",
            "สถานศึกษา": "สถานศึกษาใกล้เคียง",
            "สถานีรถไฟฟ้า": "สถานีรถไฟฟ้าใกล้เคียง",
            "ห้างสรรพสินค้า": "ห้างสรรพสินค้าใกล้เคียง"
        }
    ],
    "total": 100
}
```

## 5. การจัดการห้องสนทนา (Chat Room Management)

### สร้างห้องสนทนา (Create Chat Room)
```http
POST /api/chat-rooms
```

**Request Body:**
```json
{
    "user_id": "user_id"
}
```

**Response:**
```json
{
    "id": "chat_room_id",
    "user_id": "user_id",
    "created_at": "2024-04-21T08:00:00Z"
}
```

### ดึงประวัติการสนทนา (Get Chat History)
```http
GET /api/chat-rooms/{chat_room_id}/messages
```

**Response:**
```json
{
    "messages": [
        {
            "role": "user",
            "content": "ข้อความของผู้ใช้",
            "timestamp": 1711008000000
        },
        {
            "role": "assistant",
            "content": "คำตอบจาก AI",
            "timestamp": 1711008001000,
            "properties": []
        }
    ]
}
```

## 6. การจัดการผู้ใช้ (User Management)

### ดึงข้อมูลผู้ใช้ (Get User Profile)
```http
GET /api/users/{user_id}
```

**Response:**
```json
{
    "id": "user_id",
    "name": "ชื่อผู้ใช้",
    "email": "email@example.com",
    "created_at": "2024-04-21T08:00:00Z",
    "updated_at": "2024-04-21T08:00:00Z"
}
```

### อัปเดตข้อมูลผู้ใช้ (Update User Profile)
```http
PUT /api/users/{user_id}
```

**Request Body:**
```json
{
    "name": "ชื่อผู้ใช้ใหม่",
    "email": "email_new@example.com"
}
```

**Response:**
```json
{
    "id": "user_id",
    "name": "ชื่อผู้ใช้ใหม่",
    "email": "email_new@example.com",
    "created_at": "2024-04-21T08:00:00Z",
    "updated_at": "2024-04-21T08:00:00Z"
}
```

## 7. Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid request parameters",
    "details": "รายละเอียดข้อผิดพลาด"
}
```

### 401 Unauthorized
```json
{
    "error": "Unauthorized",
    "details": "กรุณาเข้าสู่ระบบ"
}
```

### 403 Forbidden
```json
{
    "error": "Forbidden",
    "details": "ไม่มีสิทธิ์เข้าถึง"
}
```

### 404 Not Found
```json
{
    "error": "Not found",
    "details": "ไม่พบข้อมูลที่ต้องการ"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "details": "เกิดข้อผิดพลาดภายในระบบ"
}
``` 