
# AI Property Consultant Backend

This is the FastAPI backend for the AI Property Consultant application. It provides API endpoints for property data processing, chat functionality, and file uploads.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB (running locally or accessible via connection string)

### Installation

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

The API will be available at http://localhost:8000

## API Endpoints

### Chat Endpoint

```
POST /api/chat
```

Request body:
```json
{
  "query": "ต้องการซื้อคอนโดใกล้ BTS",
  "consultation_style": "formal",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "response": "สำหรับคำถามเกี่ยวกับ 'ต้องการซื้อคอนโดใกล้ BTS' ทางเรามีข้อมูลอสังหาริมทรัพย์ที่น่าสนใจดังนี้...",
  "session_id": "session_12345abcde",
  "properties": [...]
}
```

### File Upload Endpoint

```
POST /api/upload
```

Form data:
- `file`: Excel or CSV file with property data
- `consultation_style`: Consultation style (optional)

Response:
```json
{
  "message": "อัพโหลดข้อมูลอสังหาริมทรัพย์สำเร็จ",
  "file_id": "upload_12345abcde",
  "num_records": 42
}
```

### Get Consultation Styles

```
GET /api/styles
```

Response:
```json
{
  "formal": "ทางการ",
  "casual": "ทั่วไป",
  "friendly": "เป็นกันเอง",
  "professional": "มืออาชีพ"
}
```

## File Upload Format

The uploaded Excel or CSV file should contain the following columns (in Thai):

- ประเภท (Type) - บ้าน/คอนโด/ทาวน์โฮม, etc.
- โครงการ (Project name)
- ราคา (Price)
- รูปแบบ (Format) - เช่า/ขาย (Rent/Sell)
- รูป (Image) - URL to property image
- ตำแหน่ง (Location)
- สถานศึกษา (Educational institutions nearby)
- สถานีรถไฟฟ้า (BTS/MRT stations nearby)
- ห้างสรรพสินค้า (Shopping malls nearby)
- โรงพยาบาล (Hospitals nearby)
- สนามบิน (Airports nearby)

Missing data should be filled with "ไม่มี" (None/Not available).
