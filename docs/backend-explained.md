# รายละเอียดระบบ Backend

## 1. โครงสร้างไฟล์

### 1.1 ไฟล์หลัก
- `main.py` - FastAPI application และ API endpoints
- `mongodb_manager.py` - จัดการการเชื่อมต่อและการทำงานกับ MongoDB
- `language_models.py` - ระบบประมวลผลภาษาและสร้างคำตอบ
- `vector_store.py` - ระบบค้นหาแบบ Vector Search
- `config.py` - การตั้งค่าระบบ
- `requirements.txt` - รายการ dependencies

### 1.2 การจัดการข้อมูล
- การเชื่อมต่อ MongoDB
- การจัดการ Session
- การจัดการผู้ใช้
- การจัดเก็บประวัติการสนทนา

## 2. API Endpoints

### 2.1 Chat API
```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat(query: PropertyQuery)
```
- รับคำถามจากผู้ใช้
- ประมวลผลและค้นหาข้อมูล
- สร้างคำตอบที่เหมาะสม
- จัดการประวัติการสนทนา

### 2.2 User Management
```python
@app.post("/api/register", response_model=UserResponse)
async def register_user(user_data: UserRegisterRequest)

@app.post("/api/login", response_model=UserResponse)
async def login_user(user_data: UserLoginRequest)
```
- ลงทะเบียนผู้ใช้ใหม่
- เข้าสู่ระบบ
- จัดการข้อมูลผู้ใช้

### 2.3 Data Management
```python
@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile)

@app.get("/api/styles")
async def get_consultation_styles()
```
- อัพโหลดข้อมูลอสังหาริมทรัพย์
- จัดการรูปแบบการให้คำปรึกษา

## 3. การประมวลผลข้อความ

### 3.1 การวิเคราะห์คำถาม
```python
def get_empathetic_message(query: str, property_type: str, language: str) -> str:
    # วิเคราะห์อารมณ์และความต้องการ
    # สร้างข้อความตอบกลับที่เหมาะสม
```

### 3.2 การค้นหาข้อมูล
```python
def vector_search(query: str, top_k: int = 3, language: str = "thai") -> List[Dict[str, Any]]:
    # แปลงคำถามเป็นเวกเตอร์
    # ค้นหาอสังหาริมทรัพย์ที่เกี่ยวข้อง
    # จัดอันดับผลลัพธ์
```

## 4. การจัดการฐานข้อมูล

### 4.1 MongoDB Manager
```python
class MongoDBManager:
    def __init__(self):
        # เชื่อมต่อ MongoDB
        # สร้าง collections

    def store_properties(self, properties: List[Dict[str, Any]], file_id: str) -> str:
        # บันทึกข้อมูลอสังหาริมทรัพย์

    def save_chat_room(self, chat_room_id: str, messages: List[Dict[str, Any]], user_id: Optional[str] = None) -> bool:
        # บันทึกประวัติการสนทนา
```

### 4.2 Vector Store
```python
class VectorStore:
    def __init__(self, embedding_model_name: str = None):
        # ตั้งค่าระบบ Vector Search

    def search(self, query: str, top_k: int = MAX_RESULTS) -> List[Dict[str, Any]]:
        # ค้นหาข้อมูลด้วย Vector Similarity
```

## 5. การจัดการภาษา

### 5.1 Language Models
```python
class LanguageModelManager:
    def generate_response(self, query: str, properties: List[Dict[str, Any]], style: str = "formal") -> str:
        # สร้างคำตอบตามรูปแบบที่กำหนด

    def translate(self, text: str, target_language: str = "en") -> str:
        # แปลภาษาตามที่ต้องการ
```

## 6. การรักษาความปลอดภัย

### 6.1 Authentication
- JWT Tokens
- Session Management
- Password Hashing

### 6.2 Data Protection
- Input Validation
- Error Handling
- Rate Limiting

## 7. การจัดการ Error

### 7.1 Error Handling
```python
try:
    # ดำเนินการ
except Exception as e:
    logger.error(f"Error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### 7.2 Logging
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 8. การตั้งค่าระบบ

### 8.1 Configuration
```python
# config.py
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/AI")
MONGODB_DB = os.getenv("MONGODB_DB", "AI")
```

### 8.2 Dependencies
```
fastapi==0.68.0
pymongo==3.12.0
python-multipart==0.0.5
pandas==1.3.0
``` 