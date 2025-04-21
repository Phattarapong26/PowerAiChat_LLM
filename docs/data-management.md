# การจัดการข้อมูล

## ภาพรวม

การจัดการข้อมูลในระบบ AI Property Consultant เป็นกระบวนการที่สำคัญในการดูแลข้อมูลอสังหาริมทรัพย์ ข้อมูลผู้ใช้ และข้อมูลการสนทนา เพื่อให้ระบบสามารถทำงานได้อย่างมีประสิทธิภาพ

## โครงสร้างข้อมูล

### ข้อมูลอสังหาริมทรัพย์
```python
property_schema = {
    "property_id": str,
    "title": str,
    "description": str,
    "price": float,
    "location": {
        "address": str,
        "district": str,
        "province": str,
        "coordinates": {
            "latitude": float,
            "longitude": float
        }
    },
    "features": {
        "bedrooms": int,
        "bathrooms": int,
        "area": float,
        "property_type": str,
        "facilities": list[str]
    },
    "images": list[str],
    "status": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

### ข้อมูลผู้ใช้
```python
user_schema = {
    "user_id": str,
    "username": str,
    "email": str,
    "password": str,
    "profile": {
        "name": str,
        "phone": str,
        "preferences": {
            "property_types": list[str],
            "price_range": {
                "min": float,
                "max": float
            },
            "locations": list[str]
        }
    },
    "role": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

### ข้อมูลการสนทนา
```python
chat_schema = {
    "chat_id": str,
    "user_id": str,
    "messages": [
        {
            "message_id": str,
            "content": str,
            "role": str,
            "timestamp": datetime
        }
    ],
    "property_id": str,
    "status": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

## การจัดการข้อมูล

### การเพิ่มข้อมูล
```python
def add_property(property_data: dict) -> str:
    # ตรวจสอบความถูกต้องของข้อมูล
    validate_property_data(property_data)
    
    # เพิ่มข้อมูลลงในฐานข้อมูล
    property_id = mongodb_manager.add_property(property_data)
    
    # สร้างเวกเตอร์สำหรับการค้นหา
    vector_store.add_property(property_id, property_data)
    
    return property_id
```

### การอัปเดตข้อมูล
```python
def update_property(property_id: str, property_data: dict) -> bool:
    # ตรวจสอบความถูกต้องของข้อมูล
    validate_property_data(property_data)
    
    # อัปเดตข้อมูลในฐานข้อมูล
    success = mongodb_manager.update_property(property_id, property_data)
    
    if success:
        # อัปเดตเวกเตอร์สำหรับการค้นหา
        vector_store.update_property(property_id, property_data)
    
    return success
```

### การลบข้อมูล
```python
def delete_property(property_id: str) -> bool:
    # ลบข้อมูลจากฐานข้อมูล
    success = mongodb_manager.delete_property(property_id)
    
    if success:
        # ลบเวกเตอร์จากการค้นหา
        vector_store.delete_property(property_id)
    
    return success
```

## การสำรองข้อมูล

### การสำรองข้อมูลอัตโนมัติ
```python
def backup_data():
    # สำรองข้อมูลอสังหาริมทรัพย์
    mongodb_manager.backup_properties()
    
    # สำรองข้อมูลผู้ใช้
    mongodb_manager.backup_users()
    
    # สำรองข้อมูลการสนทนา
    mongodb_manager.backup_chats()
    
    # สำรองเวกเตอร์
    vector_store.backup_vectors()
```

### การกู้คืนข้อมูล
```python
def restore_data(backup_id: str):
    # กู้คืนข้อมูลอสังหาริมทรัพย์
    mongodb_manager.restore_properties(backup_id)
    
    # กู้คืนข้อมูลผู้ใช้
    mongodb_manager.restore_users(backup_id)
    
    # กู้คืนข้อมูลการสนทนา
    mongodb_manager.restore_chats(backup_id)
    
    # กู้คืนเวกเตอร์
    vector_store.restore_vectors(backup_id)
```

## การทำความสะอาดข้อมูล

### การตรวจสอบความถูกต้อง
```python
def validate_data():
    # ตรวจสอบความถูกต้องของข้อมูลอสังหาริมทรัพย์
    validate_properties()
    
    # ตรวจสอบความถูกต้องของข้อมูลผู้ใช้
    validate_users()
    
    # ตรวจสอบความถูกต้องของข้อมูลการสนทนา
    validate_chats()
```

### การแก้ไขข้อมูล
```python
def clean_data():
    # แก้ไขข้อมูลอสังหาริมทรัพย์
    clean_properties()
    
    # แก้ไขข้อมูลผู้ใช้
    clean_users()
    
    # แก้ไขข้อมูลการสนทนา
    clean_chats()
```

## การตรวจสอบประสิทธิภาพ

### เมตริกการประเมิน
- **ความถูกต้อง**: วัดความถูกต้องของข้อมูล
- **ความสมบูรณ์**: วัดความสมบูรณ์ของข้อมูล
- **ความสอดคล้อง**: วัดความสอดคล้องของข้อมูล
- **ประสิทธิภาพ**: วัดประสิทธิภาพของการจัดการข้อมูล

### การปรับปรุงประสิทธิภาพ
```python
def improve_data_management():
    # ปรับปรุงการจัดการข้อมูล
    optimize_database()
    
    # ปรับปรุงการสำรองข้อมูล
    optimize_backup()
    
    # ปรับปรุงการทำความสะอาดข้อมูล
    optimize_cleaning()
``` 