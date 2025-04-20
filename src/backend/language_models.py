
import logging
from typing import Dict, Any, List
from config import MODEL_CONFIG, CONSULTATION_STYLES

logger = logging.getLogger(__name__)

class LanguageModelManager:
    def __init__(self):
        """
        Manages language model interactions for the AI property consultant
        
        In production, this would connect to actual language models.
        For this demo, we'll use templates.
        """
        self.model_config = MODEL_CONFIG
        logger.info(f"Initialized LanguageModelManager with config: {MODEL_CONFIG}")
        
    def generate_response(self, 
                          query: str, 
                          properties: List[Dict[str, Any]], 
                          style: str = "formal", 
                          context: List[Dict[str, Any]] = None) -> str:
        """
        Generate AI response based on query, matched properties, and consultation style
        """
        try:
            # Check if we found any properties
            if not properties:
                responses = {
                    "formal": f"ขออภัยครับ ทางเราไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงกับคำถาม '{query}' กรุณาลองใช้คำค้นหาอื่น หรือติดต่อเจ้าหน้าที่เพื่อขอข้อมูลเพิ่มเติม",
                    "casual": f"เราไม่เจอข้อมูลที่คุณถามเกี่ยวกับ '{query}' ลองถามใหม่ด้วยคำอื่นได้นะ หรือจะติดต่อเจ้าหน้าที่ก็ได้ครับ",
                    "friendly": f"โอ้! ดูเหมือนว่าเรายังไม่มีข้อมูลเกี่ยวกับ '{query}' เลย ลองถามใหม่แบบอื่นไหมคะ หรือจะคุยกับพนักงานของเราโดยตรงก็ได้นะคะ",
                    "professional": f"ผมขอแจ้งว่าไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงตามเงื่อนไข '{query}' ในระบบ ผมแนะนำให้ปรับเปลี่ยนคำค้นหา หรือหากต้องการความช่วยเหลือเพิ่มเติม สามารถติดต่อทีมงานมืออาชีพของเราได้ครับ"
                }
                return responses.get(style, responses["formal"])
            
            # Create property description based on the data
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
        Translate text between Thai and English
        
        This would use an actual translation model in production
        """
        logger.info(f"Translation requested to {target_language}")
        # Mock implementation
        return f"[Translated to {target_language}]: {text}"
