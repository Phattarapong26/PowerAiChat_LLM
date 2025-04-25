import logging
from typing import Dict, Any, List
from transformers import AutoTokenizer, AutoModelForCausalLM
# ใช้ meta-llama/Llama-3.2-1B สำหรับทุกการ generate
from config import MODEL_CONFIG, CONSULTATION_STYLES

logger = logging.getLogger(__name__)

class LanguageModelManager:
    # ระบบนี้รองรับเฉพาะภาษาไทยเท่านั้น (Thai only)
    def __init__(self):
        """
        Manages language model interactions for the AI property consultant
        """
        self.model_config = MODEL_CONFIG
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
        self.model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
        # Ensure pad_token exists for generation
        if self.tokenizer.pad_token is None:
            if self.tokenizer.eos_token is not None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            else:
                self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
                self.model.resize_token_embeddings(len(self.tokenizer))
        logger.info("Initialized LanguageModelManager with meta-llama/Llama-3.2-1B model (pad_token_id={})".format(self.tokenizer.pad_token_id))
        
    def generate_fallback_response(self, query: str, style: str) -> str:
        """
        Generate fallback response using meta-llama/Llama-3.2-1B
        """
        try:
            prompt = f"""
            คุณเป็นที่ปรึกษาอสังหาริมทรัพย์ที่พูดภาษาไทย
            ลูกค้าถามว่า: {query}
            แต่เราไม่พบอสังหาริมทรัพย์ที่ตรงตามเงื่อนไข
            กรุณาตอบในรูปแบบ {style} โดยแสดงความเห็นอกเห็นใจและแนะนำทางเลือกอื่น
            """
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True, padding=True)
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=150,
                min_new_tokens=30,
                do_sample=True,
                num_beams=3,
                temperature=0.8,
                top_p=0.95,
                top_k=40,
                repetition_penalty=1.3,
                no_repeat_ngram_size=4,
                length_penalty=1.2,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if not response.strip():
                # ถ้ายังว่างเปล่าอีก ให้ใช้ fallback แบบ hardcoded
                fallback_responses = {
                    "formal": "ขออภัยครับ ทางเราไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงกับคำถาม กรุณาลองใช้คำค้นหาอื่น หรือติดต่อเจ้าหน้าที่เพื่อขอข้อมูลเพิ่มเติม",
                    "casual": "เราไม่เจอข้อมูลที่คุณถาม ลองถามใหม่ด้วยคำอื่นได้นะ หรือจะติดต่อเจ้าหน้าที่ก็ได้ครับ",
                    "friendly": "อุ๊ย! ขอโทษนะคะ ยังไม่เจอที่ตรงใจเลย ลองถามใหม่แบบอื่นไหมคะ หรือจะคุยกับพนักงานของเราโดยตรงก็ได้นะคะ",
                    "professional": "ผมขอแจ้งว่าไม่พบข้อมูลอสังหาริมทรัพย์ที่ตรงตามเงื่อนไขในระบบ ผมแนะนำให้ปรับเปลี่ยนคำค้นหา หรือหากต้องการความช่วยเหลือเพิ่มเติม สามารถติดต่อทีมงานมืออาชีพของเราได้ครับ"
                }
                return fallback_responses.get(style, fallback_responses["formal"])
            return response
        except Exception as e:
            logger.error(f"Error generating fallback response: {str(e)}")
            return "ขออภัย เกิดข้อผิดพลาดในการประมวลผลคำตอบ กรุณาลองใหม่อีกครั้ง"
        
    def generate_response(self, 
                          query: str, 
                          properties: List[Dict[str, Any]], 
                          style: str = "formal", 
                          context: List[Dict[str, Any]] = None) -> str:
        """
        Generate AI response based on query, matched properties, and consultation style (meta-llama/Llama-3.2-1B)
        """
        try:
            # Check if we found any properties
            if not properties:
                prompt = f"""
                คุณเป็นที่ปรึกษาอสังหาริมทรัพย์ที่พูดภาษาไทย
                ลูกค้าถามว่า: {query}
                แต่เราไม่พบอสังหาริมทรัพย์ที่ตรงตามเงื่อนไข
                กรุณาตอบในรูปแบบ {style} โดยแสดงความเห็นอกเห็นใจและแนะนำทางเลือกอื่น
                """
                inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True, padding=True)
                outputs = self.model.generate(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_new_tokens=150,
                    min_new_tokens=30,
                    do_sample=True,
                    num_beams=3,
                    temperature=0.8,
                    top_p=0.95,
                    top_k=40,
                    repetition_penalty=1.3,
                    no_repeat_ngram_size=4,
                    length_penalty=1.2,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                # ตรวจสอบว่าคำตอบไม่ว่างเปล่า
                if not response.strip():
                    logger.warning("Empty response from model, using fallback response")
                    return self.generate_fallback_response(query, style)
                return response
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
            prompt = f"""
            คุณเป็นที่ปรึกษาอสังหาริมทรัพย์ที่พูดภาษาไทย
            ลูกค้าถามว่า: {query}
            \nคุณพบอสังหาริมทรัพย์ที่ตรงตามเงื่อนไขดังนี้:
            {property_text}
            \nกรุณาตอบในรูปแบบ {style} โดยแนะนำอสังหาริมทรัพย์เหล่านี้ให้ลูกค้า
            """
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True, padding=True)
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=150,
                min_new_tokens=30,
                do_sample=True,
                num_beams=3,
                temperature=0.8,
                top_p=0.95,
                top_k=40,
                repetition_penalty=1.3,
                no_repeat_ngram_size=4,
                length_penalty=1.2,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # ตรวจสอบว่าคำตอบไม่ว่างเปล่า
            if not response.strip():
                logger.warning("Empty response from model, using fallback response")
                return self.generate_fallback_response(query, style)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "ขออภัย เกิดข้อผิดพลาดในการประมวลผลคำตอบ กรุณาลองใหม่อีกครั้ง"
            
    def translate(self, text: str, target_language: str = "en") -> str:
        """
        แปลข้อความโดยใช้ meta-llama/Llama-3.2-1B (ควร fine-tune เพิ่มเติมกรณี production)
        """
        logger.info(f"Translation requested to {target_language}")
        prompt = f"Translate the following text to {target_language}: {text}"
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True, padding=True)
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=150,
            min_new_tokens=30,
            do_sample=True,
            num_beams=3,
            temperature=0.8,
            top_p=0.95,
            top_k=40,
            repetition_penalty=1.3,
            no_repeat_ngram_size=4,
            length_penalty=1.2,
            early_stopping=True,
            pad_token_id=self.tokenizer.pad_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
