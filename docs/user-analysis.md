# User Analysis Documentation

## ภาพรวม

ระบบวิเคราะห์ผู้ใช้ (User Analyzer) ถูกออกแบบมาเพื่อวิเคราะห์ความสนใจและความต้องการของผู้ใช้จากข้อความที่ส่งมา โดยใช้เทคนิค Vector Search และการแยกประเภทอสังหาริมทรัพย์และตำแหน่ง

## การวิเคราะห์ความสนใจ

### 1. การแยกประเภทอสังหาริมทรัพย์
```python
def _extract_property_type(self, query: str) -> str:
    """
    แยกประเภทอสังหาริมทรัพย์จากประโยคค้นหา
    """
    property_types = {
        'กิจการ': ['กิจการ', 'ธุรกิจ', 'ร้าน', 'ร้านค้า', 'ร้านอาหาร', 'ร้านกาแฟ', 'ร้านเสริมสวย'],
        'คอนโด': ['คอนโด', 'คอนโดมิเนียม', 'อพาร์ตเมนต์', 'ห้องชุด', 'ห้องพัก'],
        'ทาวน์โฮม': ['ทาวน์โฮม', 'ทาวน์เฮ้าส์', 'บ้านแฝด', 'บ้านแถว'],
        'ที่ดิน': ['ที่ดิน', 'ที่ว่าง', 'ที่เปล่า', 'ที่เปล่าเปล่า', 'ที่ดินเปล่า'],
        'บ้าน': ['บ้าน', 'บ้านเดี่ยว', 'บ้านสองชั้น', 'บ้านชั้นเดียว', 'บ้านสไตล์'],
        'ร้านค้า': ['ร้านค้า', 'ร้าน', 'ร้านขายของ', 'ร้านขายปลีก', 'ร้านค้าปลีก'],
        'สำนักงาน': ['สำนักงาน', 'ออฟฟิศ', 'ที่ทำงาน', 'ห้องทำงาน'],
        'โฮมออฟฟิศ': ['โฮมออฟฟิศ', 'บ้านสำนักงาน', 'บ้านออฟฟิศ', 'บ้านที่ทำงาน']
    }
    
    query_lower = query.lower()
    for prop_type, keywords in property_types.items():
        if any(keyword in query_lower for keyword in keywords):
            return prop_type
    return ""
```

### 2. การแยกตำแหน่ง
```python
def _extract_location(self, query: str) -> str:
    """
    แยกตำแหน่งจากประโยคค้นหา
    """
    common_locations = [
        'บางนา', 'สุขุมวิท', 'รัชดา', 'ลาดพร้าว', 'พระราม 9',
        'สีลม', 'สาทร', 'ทองหล่อ', 'เอกมัย', 'อโศก',
        'ราชดำริ', 'พร้อมพงษ์', 'ทองหล่อ', 'อ่อนนุช', 'บางกะปิ',
        'ลาดกระบัง', 'มีนบุรี', 'บางแค', 'บางบอน', 'บางขุนเทียน'
    ]
    
    words = query.split()
    for word in words:
        if word in common_locations:
            return word
    return ""
```

### 3. การวิเคราะห์ความสนใจ
```python
async def analyze_user_interests(self, query: str, consultation_style: str = "formal", language: str = "thai") -> Dict[str, Any]:
    """
    วิเคราะห์ความสนใจของผู้ใช้จากข้อความที่ส่งมา
    """
    try:
        # ตรวจสอบว่ามี MongoDB manager และ session หรือไม่
        if not hasattr(self, 'mongo_manager') or not hasattr(self, 'session'):
            return {
                "interests": [],
                "location_preferences": [],
                "budget_range": None,
                "property_type": None,
                "error": "Database connection not available"
            }

        # แยกประเภทอสังหาริมทรัพย์และตำแหน่งจากคำค้นหา
        detected_property_type = self._extract_property_type(query)
        detected_location = self._extract_location(query)

        # ดึงข้อความจาก chat messages
        chat_messages = await self.mongo_manager.get_chat_messages(
            self.session,
            query
        )

        # สร้าง vector store สำหรับการค้นหา
        vector_store = VectorStore()

        # ดึงข้อมูล properties ทั้งหมด
        properties = await self.mongo_manager.get_all_properties(self.session)
        
        # แปลง ObjectId เป็น string สำหรับแต่ละ property
        for prop in properties:
            prop['_id'] = str(prop['_id'])

        # เพิ่มข้อมูลลงใน vector store
        vector_store.add_properties(properties)

        # วิเคราะห์ความสนใจจากข้อความ
        analysis = vector_store.analyze_interests(query)

        # ปรับคะแนนความสนใจตามประเภทอสังหาริมทรัพย์ที่ตรวจพบ
        if detected_property_type:
            for interest in analysis["interests"]:
                if interest["property"]["ประเภท"] == detected_property_type:
                    interest["score"] *= 2.5  # เพิ่มคะแนนให้กับประเภทที่ตรงกับที่ผู้ใช้ต้องการ

        # ปรับคะแนนความสนใจตามตำแหน่งที่ตรวจพบ
        if detected_location:
            for interest in analysis["interests"]:
                if detected_location in interest["property"].get("ตำแหน่ง", ""):
                    interest["score"] *= 2.0  # เพิ่มคะแนนให้กับตำแหน่งที่ตรงกับที่ผู้ใช้ต้องการ

        # เรียงลำดับความสนใจใหม่ตามคะแนน
        analysis["interests"].sort(key=lambda x: x["score"], reverse=True)

        # เพิ่มข้อมูลประเภทอสังหาริมทรัพย์และตำแหน่งที่ตรวจพบ
        analysis["detected_property_type"] = detected_property_type
        analysis["detected_location"] = detected_location

        return analysis

    except Exception as e:
        return {
            "interests": [],
            "location_preferences": [],
            "budget_range": None,
            "property_type": None,
            "error": str(e)
        }
```

## การใช้งาน

### 1. การวิเคราะห์ความสนใจ
```python
# สร้าง UserAnalyzer
user_analyzer = UserAnalyzer(mongodb_manager)

# วิเคราะห์ความสนใจ
analysis = await user_analyzer.analyze_user_interests(
    query="ต้องการคอนโดใกล้รถไฟฟ้าสีลม",
    consultation_style="formal",
    language="thai"
)
```

### 2. การแยกประเภทและตำแหน่ง
```python
# แยกประเภทอสังหาริมทรัพย์
property_type = user_analyzer._extract_property_type("ต้องการคอนโดใกล้รถไฟฟ้าสีลม")
# ผลลัพธ์: "คอนโด"

# แยกตำแหน่ง
location = user_analyzer._extract_location("ต้องการคอนโดใกล้รถไฟฟ้าสีลม")
# ผลลัพธ์: "สีลม"
```

## การบำรุงรักษา

### การอัปเดต
- เพิ่มประเภทอสังหาริมทรัพย์ใหม่
- เพิ่มตำแหน่งใหม่
- ปรับปรุงการวิเคราะห์ความสนใจ
- เพิ่มฟีเจอร์ใหม่

### การตรวจสอบ
- ตรวจสอบความถูกต้องของการวิเคราะห์
- ติดตามประสิทธิภาพ
- วิเคราะห์ข้อผิดพลาด
- ตรวจสอบความแม่นยำ

### การสำรองข้อมูล
- สำรองข้อมูลการวิเคราะห์
- มีแผนกู้คืนเมื่อเกิดปัญหา
- ทดสอบระบบเป็นประจำ 