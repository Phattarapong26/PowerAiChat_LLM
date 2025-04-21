# AI Models Documentation

## ภาพรวม

ระบบ AI Property Consultant ใช้โมเดล AI หลักๆ ดังนี้:

1. **Language Model**
   - ใช้สำหรับการสนทนาและให้คำแนะนำเกี่ยวกับอสังหาริมทรัพย์
   - รองรับการสนทนา 4 รูปแบบ: ทางการ, ทั่วไป, เป็นกันเอง, มืออาชีพ
   - รองรับการแปลภาษาไทย-อังกฤษ

2. **Embedding Model**
   - ใช้สำหรับแปลงข้อมูลอสังหาริมทรัพย์เป็นเวกเตอร์
   - ช่วยในการค้นหาและแนะนำอสังหาริมทรัพย์ที่ตรงกับความต้องการ
   - รองรับการค้นหาแบบหลายมิติ

## Model Specifications

### Language Model
- **Model**: google/flan-t5-base
- **Capabilities**:
  - การสนทนาแบบธรรมชาติ
  - การวิเคราะห์ข้อมูลอสังหาริมทรัพย์
  - การให้คำแนะนำที่เหมาะสม
  - การแปลภาษาไทย-อังกฤษ
  - การปรับแต่งการตอบสนองตามรูปแบบการสนทนา

### Embedding Model
- **Model**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Capabilities**:
  - การแปลงข้อความเป็นเวกเตอร์
  - การค้นหาความคล้ายคลึงกัน
  - การจัดกลุ่มข้อมูล
  - การค้นหาแบบหลายมิติ

## Integration

### Language Model Integration
```python
class LanguageModelManager:
    def __init__(self):
        self.model_config = MODEL_CONFIG
        logger.info(f"Initialized LanguageModelManager with config: {MODEL_CONFIG}")
        
    def generate_response(self, query: str, properties: List[Dict[str, Any]], style: str = "formal", context: List[Dict[str, Any]] = None) -> str:
        try:
            # ตรวจสอบว่ามีข้อมูลอสังหาริมทรัพย์หรือไม่
            if not properties:
                responses = {
                    "formal": f"ขออภัยครับ ทางเราไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงกับคำถาม '{query}' กรุณาลองใช้คำค้นหาอื่น หรือติดต่อเจ้าหน้าที่เพื่อขอข้อมูลเพิ่มเติม",
                    "casual": f"เราไม่เจอข้อมูลที่คุณถามเกี่ยวกับ '{query}' ลองถามใหม่ด้วยคำอื่นได้นะ หรือจะติดต่อเจ้าหน้าที่ก็ได้ครับ",
                    "friendly": f"โอ้! ดูเหมือนว่าเรายังไม่มีข้อมูลเกี่ยวกับ '{query}' เลย ลองถามใหม่แบบอื่นไหมคะ หรือจะคุยกับพนักงานของเราโดยตรงก็ได้นะคะ",
                    "professional": f"ผมขอแจ้งว่าไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงตามเงื่อนไข '{query}' ในระบบ ผมแนะนำให้ปรับเปลี่ยนคำค้นหา หรือหากต้องการความช่วยเหลือเพิ่มเติม สามารถติดต่อทีมงานมืออาชีพของเราได้ครับ"
                }
                return responses.get(style, responses["formal"])
            
            # สร้างคำอธิบายอสังหาริมทรัพย์
            property_descriptions = []
            for i, prop in enumerate(properties):
                desc = f"{i+1}. "
                
                if "ประเภท" in prop:
                    desc += f"{prop['ประเภท']} "
                
                if "โครงการ" in prop:
                    desc += f"{prop['โครงการ']} "
                
                if "ราคา" in prop:
                    desc += f"ราคา {prop['ราคา']} บาท "
                
                if "รูปแบบ" in prop:
                    desc += f"({prop['รูปแบบ']}) "
                
                nearby = []
                if "สถานศึกษา" in prop and prop["สถานศึกษา"] != "ไม่มี":
                    nearby.append(f"ใกล้{prop['สถานศึกษา']}")
                
                if "สถานีรถไฟฟ้า" in prop and prop["สถานีรถไฟฟ้า"] != "ไม่มี":
                    nearby.append(f"ใกล้{prop['สถานีรถไฟฟ้า']}")
                    
                if "ห้างสรรพสินค้า" in prop and prop["ห้างสรรพสินค้า"] != "ไม่มี":
                    nearby.append(f"ใกล้{prop['ห้างสรรพสินค้า']}")
                    
                if nearby:
                    desc += f" {', '.join(nearby)}"
                    
                property_descriptions.append(desc)
            
            property_text = "\n".join(property_descriptions)
            
            # สร้างการตอบสนองตามรูปแบบ
            intros = {
                "formal": f"สำหรับคำถามเกี่ยวกับ '{query}' ทางเรามีข้อมูลอสังหาริมทรัพย์ที่น่าสนใจดังนี้:\n\n",
                "casual": f"เกี่ยวกับ '{query}' ที่คุณถามมา เรามีตัวเลือกเหล่านี้นะ:\n\n",
                "friendly": f"สำหรับ '{query}' ที่คุณสนใจ มีตัวเลือกน่าสนใจเหล่านี้เลยค่ะ:\n\n",
                "professional": f"ตามที่คุณสอบถามเกี่ยวกับ '{query}' ผมได้คัดสรรอสังหาริมทรัพย์ที่ตรงกับความต้องการของคุณดังนี้:\n\n"
            }
            
            outros = {
                "formal": "\n\nท่านสนใจทรัพย์สินรายการใดเป็นพิเศษหรือไม่ ทางเรายินดีให้ข้อมูลเพิ่มเติมครับ",
                "casual": "\n\nสนใจตัวไหนเป็นพิเศษมั้ย จะได้บอกรายละเอียดเพิ่มเติมให้",
                "friendly": "\n\nชอบตัวไหนเป็นพิเศษบ้างคะ บอกได้เลยนะ เดี๋ยวเราช่วยดูข้อมูลเพิ่มให้ค่ะ",
                "professional": "\n\nหากคุณสนใจอสังหาริมทรัพย์รายการใดเป็นพิเศษ ผมสามารถให้ข้อมูลเชิงลึกและจัดการดูพื้นที่จริงให้ได้ครับ"
            }
            
            intro = intros.get(style, intros["formal"])
            outro = outros.get(style, outros["formal"])
            
            return intro + property_text + outro
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "ขออภัย เกิดข้อผิดพลาดในการประมวลผลคำตอบ กรุณาลองใหม่อีกครั้ง"
            
    def translate(self, text: str, target_language: str = "en") -> str:
        """
        แปลข้อความระหว่างภาษาไทยและภาษาอังกฤษ
        """
        logger.info(f"Translation requested to {target_language}")
        return f"[Translated to {target_language}]: {text}"
```

### Embedding Model Integration
```python
class VectorStore:
    def __init__(self, embedding_model_name: str = None):
        self.embedding_model_name = embedding_model_name or MODEL_CONFIG['embedding_model']
        self.model = SentenceTransformer(self.embedding_model_name)
        self.vectors = []
        self.property_data = []
        
    def add_properties(self, properties: List[Dict[str, Any]]) -> None:
        try:
            self.property_data.extend(properties)
            texts = [self._get_property_text(prop) for prop in properties]
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            self.vectors.extend(embeddings)
        except Exception as e:
            logger.error(f"Error adding properties to vector store: {str(e)}")
            raise
```

## การบำรุงรักษา

### การอัปเดต
- อัปเดตโมเดลเป็นประจำ
- ปรับปรุงประสิทธิภาพ
- แก้ไขข้อบกพร่อง
- เพิ่มฟีเจอร์ใหม่

### การตรวจสอบ
- ตรวจสอบประสิทธิภาพของโมเดล
- ติดตามการใช้ทรัพยากร
- วิเคราะห์ข้อผิดพลาด
- ตรวจสอบความแม่นยำ

### การสำรองข้อมูล
- สำรองข้อมูลโมเดล
- มีแผนกู้คืนเมื่อเกิดปัญหา
- ทดสอบระบบเป็นประจำ 