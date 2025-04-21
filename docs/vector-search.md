# การทำงานของ Vector Search

## ภาพรวม

Vector Search เป็นเทคโนโลยีที่ใช้ในการค้นหาอสังหาริมทรัพย์ที่ตรงกับความต้องการของผู้ใช้ โดยใช้การแปลงข้อมูลเป็นเวกเตอร์และคำนวณความคล้ายคลึงกัน

## หลักการทำงาน

1. **การแปลงข้อมูลเป็นเวกเตอร์**
   - ใช้ Embedding Model แปลงข้อมูลอสังหาริมทรัพย์เป็นเวกเตอร์
   - แต่ละคุณสมบัติของอสังหาริมทรัพย์จะถูกแปลงเป็นมิติในเวกเตอร์
   - ใช้ Sentence Transformers สำหรับการแปลงข้อความเป็นเวกเตอร์

2. **การจัดเก็บเวกเตอร์**
   - เก็บเวกเตอร์ในฐานข้อมูลแบบเวกเตอร์
   - จัดทำดัชนีเพื่อเพิ่มความเร็วในการค้นหา
   - มีการอัปเดตเวกเตอร์เมื่อข้อมูลเปลี่ยนแปลง

3. **การค้นหา**
   - แปลงคำค้นหาของผู้ใช้เป็นเวกเตอร์
   - คำนวณความคล้ายคลึงกันระหว่างเวกเตอร์
   - เรียงลำดับผลลัพธ์ตามคะแนนความคล้ายคลึงกัน

## การประมวลผลข้อมูล

### การเตรียมข้อมูล
```python
def prepare_property_data(property_data: dict) -> dict:
    # แปลงข้อมูลดิบให้เป็นรูปแบบที่เหมาะสม
    processed_data = {
        "text": create_property_text(property_data),
        "features": extract_features(property_data),
        "location": process_location(property_data["location"]),
        "price": normalize_price(property_data["price"])
    }
    return processed_data
```

### การสร้างเวกเตอร์
```python
def create_embeddings(data: dict) -> np.ndarray:
    # สร้างเวกเตอร์จากข้อมูล
    text_embedding = get_text_embedding(data["text"])
    feature_embedding = get_feature_embedding(data["features"])
    location_embedding = get_location_embedding(data["location"])
    price_embedding = get_price_embedding(data["price"])
    
    # รวมเวกเตอร์ทั้งหมด
    combined_embedding = np.concatenate([
        text_embedding,
        feature_embedding,
        location_embedding,
        price_embedding
    ])
    return combined_embedding
```

### การค้นหา
```python
def search_similar_properties(query: str, top_k: int = 5) -> list[dict]:
    # แปลงคำค้นหาเป็นเวกเตอร์
    query_embedding = get_text_embedding(query)
    
    # ค้นหาอสังหาริมทรัพย์ที่คล้ายกัน
    results = vector_store.search(
        query_embedding,
        top_k=top_k,
        similarity_threshold=0.7
    )
    
    return results
```

## การประมวลผลข้อมูล

### การเตรียมข้อมูล
```python
def prepare_property_data(property_data: dict) -> dict:
    # แปลงข้อมูลดิบให้เป็นรูปแบบที่เหมาะสม
    processed_data = {
        "text": create_property_text(property_data),
        "features": extract_features(property_data),
        "location": process_location(property_data["location"]),
        "price": normalize_price(property_data["price"])
    }
    return processed_data
```

### การสร้างเวกเตอร์
```python
def create_embeddings(data: dict) -> np.ndarray:
    # สร้างเวกเตอร์จากข้อมูล
    text_embedding = get_text_embedding(data["text"])
    feature_embedding = get_feature_embedding(data["features"])
    location_embedding = get_location_embedding(data["location"])
    price_embedding = get_price_embedding(data["price"])
    
    # รวมเวกเตอร์ทั้งหมด
    combined_embedding = np.concatenate([
        text_embedding,
        feature_embedding,
        location_embedding,
        price_embedding
    ])
    return combined_embedding
```

### การค้นหา
```python
def search_similar_properties(query: str, top_k: int = 5) -> list[dict]:
    # แปลงคำค้นหาเป็นเวกเตอร์
    query_embedding = get_text_embedding(query)
    
    # ค้นหาอสังหาริมทรัพย์ที่คล้ายกัน
    results = vector_store.search(
        query_embedding,
        top_k=top_k,
        similarity_threshold=0.7
    )
    
    return results
```

## การประเมินประสิทธิภาพ

### เมตริกการประเมิน
- **Recall**: วัดความสามารถในการค้นหาข้อมูลที่เกี่ยวข้องทั้งหมด
- **Precision**: วัดความแม่นยำของผลลัพธ์ที่ได้
- **Response Time**: วัดเวลาที่ใช้ในการค้นหา
- **User Satisfaction**: วัดความพึงพอใจของผู้ใช้

### การปรับปรุงประสิทธิภาพ
```python
def optimize_search_performance():
    # ปรับปรุงดัชนี
    vector_store.optimize_index()
    
    # ปรับปรุงการคำนวณความคล้ายคลึงกัน
    vector_store.update_similarity_metric()
    
    # ปรับปรุงการกรองผลลัพธ์
    vector_store.update_filtering_strategy()
```

## การบำรุงรักษา

### การอัปเดตข้อมูล
- อัปเดตเวกเตอร์เมื่อข้อมูลเปลี่ยนแปลง
- ปรับปรุงดัชนีเป็นประจำ
- ทดสอบความถูกต้องของผลลัพธ์

### การตรวจสอบประสิทธิภาพ
- ตรวจสอบความเร็วในการค้นหา
- ตรวจสอบความแม่นยำของผลลัพธ์
- ตรวจสอบการใช้ทรัพยากร

### การสำรองข้อมูล
- สำรองเวกเตอร์และดัชนี
- มีแผนกู้คืนเมื่อเกิดปัญหา
- ทดสอบระบบเป็นประจำ 