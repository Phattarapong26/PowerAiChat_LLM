from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import io
import logging
import os
from datetime import datetime, timedelta
import time
import secrets
import traceback
import random
import json
from mongodb_manager import MongoDBManager
from vector_store import VectorStore

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Property Consultant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MongoDB manager
mongodb_manager = MongoDBManager()

# Create models for request/response
class PropertyQuery(BaseModel):
    query: str
    consultation_style: str = "formal"
    session_id: Optional[str] = None
    chat_room_id: Optional[str] = None
    save_message: Optional[bool] = False
    timestamp: Optional[int] = None
    get_history: Optional[bool] = False
    language: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    chat_room_id: Optional[str] = None
    properties: Optional[List[Dict[str, Any]]] = None
    messages: Optional[List[Dict[str, Any]]] = None

class UploadResponse(BaseModel):
    message: str
    file_id: str
    num_records: int

class ChatHistoryRequest(BaseModel):
    chat_room_id: str
    messages: List[Dict[str, Any]]
    user_id: Optional[str] = None

# เพิ่มโมเดลสำหรับการลงทะเบียนและเข้าสู่ระบบ
class UserRegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    success: bool
    message: str

# Mock database for development
property_data = []
user_sessions = {}

# Consultation styles with Thai descriptions
CONSULTATION_STYLES = {
    "formal": "ทางการ", 
    "casual": "ทั่วไป", 
    "friendly": "เป็นกันเอง", 
    "professional": "มืออาชีพ"
}

def calculate_relevance(query: str, item_text: str) -> float:
    """
    คำนวณความเกี่ยวข้องระหว่าง query และข้อมูลอสังหาริมทรัพย์
    """
    try:
        # แปลง query เป็นคำๆ
        query_words = set(query.lower().split())
        
        # นับจำนวนคำที่ตรงกัน
        matches = sum(1 for word in query_words if word in item_text)
        
        # คำนวณคะแนนความเกี่ยวข้อง
        relevance = matches / len(query_words) if query_words else 0
        
        # เพิ่มน้ำหนักให้กับคำที่ตรงกันมากกว่า
        if relevance > 0.5:
            relevance *= 1.5
        
        return relevance
    except Exception as e:
        logger.error(f"Error calculating relevance: {str(e)}")
        return 0

def vector_search(query: str, top_k: int = 3, language: str = "thai") -> List[Dict[str, Any]]:
    """
    ค้นหาข้อมูลอสังหาริมทรัพย์ที่เกี่ยวข้องกับคำค้นหาโดยใช้ Vector Search
    """
    try:
        # สร้าง instance ของ VectorStore
        vector_store = VectorStore()
        
        # ดึงข้อมูลทั้งหมดจาก MongoDB
        properties = list(mongodb_manager.properties.find())
        
        # แปลง ObjectId เป็น string
        for prop in properties:
            if '_id' in prop:
                prop['_id'] = str(prop['_id'])
        
        # เพิ่มข้อมูลลงใน vector store
        vector_store.add_properties(properties)
        
        # ค้นหาข้อมูลที่เกี่ยวข้อง
        results = vector_store.search(query, top_k=top_k)
        
        # แปลงข้อมูลเป็นภาษาอังกฤษถ้าต้องการ
        if language == "english":
            results = [translate_property_data(item) for item in results]
            
        return results
        
    except Exception as e:
        logger.error(f"Error in vector search: {str(e)}")
        return []

# Format property response based on missing data
def format_property_response(properties):
    """
    Formats property data by removing fields with value 'ไม่มี', None, or 'N/A'
    """
    formatted = []
    for prop in properties:
        formatted_prop = {}
        for key, value in prop.items():
            if value not in ["ไม่มี", None, "N/A", "none", "None"]:
                formatted_prop[key] = value
        formatted.append(formatted_prop)
    return formatted



def get_empathetic_message(query: str, property_type: str, language: str) -> str:
    # คำที่เกี่ยวข้องกับอารมณ์เชิงบวก
    positive_emotions = {
        "thai": ["ดี", "ชอบ", "สนใจ", "อยาก", "ต้องการ", "กำลังมองหา", "กำลังหา", "กำลังดู"],
        "english": ["good", "like", "interested", "want", "need", "looking for", "searching", "checking"]
    }
    
    # คำที่เกี่ยวข้องกับอารมณ์เชิงลบ
    negative_emotions = {
        "thai": ["ยาก", "แพง", "ไกล", "ไม่ชอบ", "ไม่ดี", "ไม่สะดวก", "ไม่พอใจ", "ไม่มั่นใจ"],
        "english": ["difficult", "expensive", "far", "don't like", "not good", "inconvenient", "unsatisfied", "unsure"]
    }
    
    # คำที่เกี่ยวข้องกับความกังวล
    concern_emotions = {
        "thai": ["กังวล", "กลัว", "ไม่แน่ใจ", "สงสัย", "คิดมาก", "หนักใจ", "เป็นห่วง"],
        "english": ["worried", "afraid", "unsure", "wonder", "concerned", "anxious", "doubtful"]
    }
    
    # คำที่เกี่ยวข้องกับความต้องการ
    need_keywords = {
        "thai": ["ต้องการ", "อยากได้", "จำเป็น", "สำคัญ", "ต้องมี", "ขาดไม่ได้"],
        "english": ["need", "want", "require", "important", "must have", "essential"]
    }
    
    # คำที่เกี่ยวข้องกับความสนใจ
    interest_keywords = {
        "thai": ["สนใจ", "อยากรู้", "อยากทราบ", "อยากดู", "อยากเห็น", "อยากลอง"],
        "english": ["interested", "curious", "want to know", "want to see", "want to try"]
    }

    # ตรวจสอบอารมณ์จากข้อความ
    query_lower = query.lower()
    detected_emotions = []
    
    # ตรวจสอบอารมณ์เชิงบวก
    if any(word in query_lower for word in positive_emotions[language]):
        detected_emotions.append("positive")
    
    # ตรวจสอบอารมณ์เชิงลบ
    if any(word in query_lower for word in negative_emotions[language]):
        detected_emotions.append("negative")
    
    # ตรวจสอบความกังวล
    if any(word in query_lower for word in concern_emotions[language]):
        detected_emotions.append("concerned")
    
    # ตรวจสอบความต้องการ
    if any(word in query_lower for word in need_keywords[language]):
        detected_emotions.append("needy")
    
    # ตรวจสอบความสนใจ
    if any(word in query_lower for word in interest_keywords[language]):
        detected_emotions.append("interested")

    # สร้างข้อความตอบสนองตามอารมณ์ที่ตรวจพบ
    if language == "english":
        if "positive" in detected_emotions:
            return "I can feel your enthusiasm! "
        elif "negative" in detected_emotions:
            return "I understand your concerns, and I'm here to help find the right solution. "
        elif "concerned" in detected_emotions:
            return "I hear your worries, and I want to assure you that we'll find the best option together. "
        elif "needy" in detected_emotions:
            return "I understand this is important to you, and I'm committed to finding exactly what you need. "
        elif "interested" in detected_emotions:
            return "I appreciate your interest, and I'm excited to show you some great options! "
        else:
            return "I understand you're looking for something special. "
    else:
        if "positive" in detected_emotions:
            return "รู้สึกได้ถึงความสนใจของคุณเลยค่ะ! "
        elif "negative" in detected_emotions:
            return "เข้าใจความกังวลของคุณค่ะ เดี๋ยวเรามาช่วยหาทางออกที่ดีที่สุดด้วยกันนะคะ "
        elif "concerned" in detected_emotions:
            return "เข้าใจความกังวลของคุณค่ะ ไม่ต้องกังวลไปนะคะ เดี๋ยวเรามาช่วยหาตัวเลือกที่ดีที่สุดด้วยกัน "
        elif "needy" in detected_emotions:
            return "เข้าใจว่านี่เป็นสิ่งสำคัญสำหรับคุณค่ะ เดี๋ยวเรามาช่วยหาสิ่งที่ใช่ที่สุดให้คุณนะคะ "
        elif "interested" in detected_emotions:
            return "ดีใจที่คุณสนใจค่ะ เดี๋ยวเรามาดูตัวเลือกที่น่าสนใจด้วยกันนะคะ! "
        else:
            return "เข้าใจว่าคุณกำลังมองหาสิ่งพิเศษค่ะ "

def generate_ai_response(query: str, properties: List[Dict[str, Any]], consultation_style: str = "formal", language: str = "thai") -> str:
    """Generate AI response based on consultation style and language"""
    
    # เพิ่มฟังก์ชันสำหรับสร้างข้อความแสดงความเข้าใจ
    def get_empathetic_message(query: str, property_type: str, language: str) -> str:
        # คำที่เกี่ยวข้องกับอารมณ์เชิงบวก
        positive_emotions = {
            "thai": ["ดี", "ชอบ", "สนใจ", "อยาก", "ต้องการ", "กำลังมองหา", "กำลังหา", "กำลังดู"],
            "english": ["good", "like", "interested", "want", "need", "looking for", "searching", "checking"]
        }
        
        # คำที่เกี่ยวข้องกับอารมณ์เชิงลบ
        negative_emotions = {
            "thai": ["ยาก", "แพง", "ไกล", "ไม่ชอบ", "ไม่ดี", "ไม่สะดวก", "ไม่พอใจ", "ไม่มั่นใจ"],
            "english": ["difficult", "expensive", "far", "don't like", "not good", "inconvenient", "unsatisfied", "unsure"]
        }
        
        # คำที่เกี่ยวข้องกับความกังวล
        concern_emotions = {
            "thai": ["กังวล", "กลัว", "ไม่แน่ใจ", "สงสัย", "คิดมาก", "หนักใจ", "เป็นห่วง"],
            "english": ["worried", "afraid", "unsure", "wonder", "concerned", "anxious", "doubtful"]
        }
        
        # คำที่เกี่ยวข้องกับความต้องการ
        need_keywords = {
            "thai": ["ต้องการ", "อยากได้", "จำเป็น", "สำคัญ", "ต้องมี", "ขาดไม่ได้"],
            "english": ["need", "want", "require", "important", "must have", "essential"]
        }
        
        # คำที่เกี่ยวข้องกับความสนใจ
        interest_keywords = {
            "thai": ["สนใจ", "อยากรู้", "อยากทราบ", "อยากดู", "อยากเห็น", "อยากลอง"],
            "english": ["interested", "curious", "want to know", "want to see", "want to try"]
        }

        # ตรวจสอบอารมณ์จากข้อความ
        query_lower = query.lower()
        detected_emotions = []
        
        # ตรวจสอบอารมณ์เชิงบวก
        if any(word in query_lower for word in positive_emotions[language]):
            detected_emotions.append("positive")
        
        # ตรวจสอบอารมณ์เชิงลบ
        if any(word in query_lower for word in negative_emotions[language]):
            detected_emotions.append("negative")
        
        # ตรวจสอบความกังวล
        if any(word in query_lower for word in concern_emotions[language]):
            detected_emotions.append("concerned")
        
        # ตรวจสอบความต้องการ
        if any(word in query_lower for word in need_keywords[language]):
            detected_emotions.append("needy")
        
        # ตรวจสอบความสนใจ
        if any(word in query_lower for word in interest_keywords[language]):
            detected_emotions.append("interested")

        # สร้างข้อความตอบสนองตามอารมณ์ที่ตรวจพบ
        if language == "english":
            if "positive" in detected_emotions:
                return "I can feel your enthusiasm! "
            elif "negative" in detected_emotions:
                return "I understand your concerns, and I'm here to help find the right solution. "
            elif "concerned" in detected_emotions:
                return "I hear your worries, and I want to assure you that we'll find the best option together. "
            elif "needy" in detected_emotions:
                return "I understand this is important to you, and I'm committed to finding exactly what you need. "
            elif "interested" in detected_emotions:
                return "I appreciate your interest, and I'm excited to show you some great options! "
            else:
                return "I understand you're looking for something special. "
        else:
            if "positive" in detected_emotions:
                return "รู้สึกได้ถึงความสนใจของคุณเลยค่ะ! "
            elif "negative" in detected_emotions:
                return "เข้าใจความกังวลของคุณค่ะ เดี๋ยวเรามาช่วยหาทางออกที่ดีที่สุดด้วยกันนะคะ "
            elif "concerned" in detected_emotions:
                return "เข้าใจความกังวลของคุณค่ะ ไม่ต้องกังวลไปนะคะ เดี๋ยวเรามาช่วยหาตัวเลือกที่ดีที่สุดด้วยกัน "
            elif "needy" in detected_emotions:
                return "เข้าใจว่านี่เป็นสิ่งสำคัญสำหรับคุณค่ะ เดี๋ยวเรามาช่วยหาสิ่งที่ใช่ที่สุดให้คุณนะคะ "
            elif "interested" in detected_emotions:
                return "ดีใจที่คุณสนใจค่ะ เดี๋ยวเรามาดูตัวเลือกที่น่าสนใจด้วยกันนะคะ! "
            else:
                return "เข้าใจว่าคุณกำลังมองหาสิ่งพิเศษค่ะ "

    if not properties:
        if language == "english":
            no_results_responses = {
                "formal": "I understand your specific requirements, and I apologize that I couldn't find any properties matching your criteria at the moment. Would you like to explore different options?",
                "casual": "I know this might be disappointing, but I couldn't find anything matching that right now. Want to try something else?",
                "friendly": "Oh no! 😔 I really wanted to help you find the perfect place, but I couldn't find anything matching your criteria yet. Let's try something else! What kind of property are you dreaming of? 😊",
                "professional": "I acknowledge your specific requirements, however, after a thorough search, I couldn't find properties matching your criteria. Would you like to explore alternative options or refine your parameters?"
            }
        else:
            no_results_responses = {
                "formal": "ดิฉันเข้าใจความต้องการของท่าน และต้องขออภัยที่ยังไม่พบอสังหาริมทรัพย์ที่ตรงตามเงื่อนไข ต้องการลองดูตัวเลือกอื่นไหมคะ?",
                "casual": "เข้าใจว่าอาจจะผิดหวังนิดหน่อย ที่ยังไม่เจอที่ถูกใจ อยากลองหาแบบอื่นดูมั้ย?",
                "friendly": "อุ๊ย! ขอโทษนะคะ 😔 อยากจะช่วยหาที่ที่ใช่ให้คุณจริงๆ เลย แต่ยังไม่เจอที่ตรงใจ มาลองดูอย่างอื่นกันไหมคะ? คุณกำลังมองหาแบบไหนอยู่คะ? 😊",
                "professional": "ผมเข้าใจความต้องการเฉพาะของท่าน อย่างไรก็ตาม จากการค้นหาอย่างละเอียด ยังไม่พบอสังหาริมทรัพย์ที่ตรงตามเกณฑ์ ต้องการให้ช่วยหาตัวเลือกอื่น หรือปรับเงื่อนไขการค้นหาไหมครับ?"
            }
        return no_results_responses.get(consultation_style, no_results_responses["formal"])

    # สร้าง response templates ตาม style และภาษา
    if language == "english":
        response_templates = {
            "formal": {
                "intro": get_empathetic_message(query, properties[0].get("type_en", ""), language) + "Based on your search for '{query}', I've discovered some exceptional properties that perfectly align with your requirements:",
                "property": "\n\n{index}. Distinguished {type} at {project}\n   Exceptional Value: {price} THB ({status})\n   Prestigious Location: {location}\n   Premium Amenities: {nearby}",
                "outro": "\n\nI would be delighted to provide more detailed information about any of these distinguished properties. Which aspects would you like to explore further?"
            },
            "casual": {
                "intro": get_empathetic_message(query, properties[0].get("type_en", ""), language) + "Found some really awesome places that match what you're looking for:",
                "property": "\n\n{index}. Take a look at this amazing {type} at {project}\n   Sweet Deal: {price} THB ({status})\n   Cool Location: {location}\n   Awesome Stuff Nearby: {nearby}",
                "outro": "\n\nAny of these catch your eye? Just let me know which one you're curious about and I'll tell you all about it!"
            },
            "friendly": {
                "intro": get_empathetic_message(query, properties[0].get("type_en", ""), language) + "I'm so excited to show you these amazing properties I found just for you! 🤩",
                "property": "\n\n{index}. You're going to love this {type} at {project}\n   Amazing Deal: {price} THB ({status})\n   Perfect Spot: {location}\n   Fantastic Neighborhood: {nearby}",
                "outro": "\n\nIsn't this exciting? 🌟 I can't wait to tell you more about whichever one you like best! Which one makes you smile? 😊"
            },
            "professional": {
                "intro": get_empathetic_message(query, properties[0].get("type_en", ""), language) + "Following a comprehensive analysis of your requirements for '{query}', I've identified these premium properties that exceed expectations:",
                "property": "\n\n{index}. Executive {type} at {project}\n   Premium Investment: {price} THB ({status})\n   Strategic Location: {location}\n   Elite Amenities: {nearby}",
                "outro": "\n\nThese carefully curated properties represent the pinnacle of current market offerings. I'd be pleased to provide an in-depth analysis of any property that interests you."
            }
        }
    else:
        response_templates = {
            "formal": {
            "intro": get_empathetic_message(query, properties[0].get("ประเภท", ""), language) + "ตามความต้องการเกี่ยวกับ '{query}' ที่ท่านได้ระบุไว้ ดิฉันได้รวบรวมตัวเลือกอสังหาริมทรัพย์ที่น่าสนใจมาให้พิจารณาดังนี้ค่ะ:",
            "property": "\n\n{index}. {type} - {project}\n   ราคาที่เหมาะสมต่อการลงทุน: {price} บาท ({status})\n   ทำเลศักยภาพ: {location}\n   สิ่งอำนวยความสะดวกที่ตอบโจทย์การใช้ชีวิต: {nearby}",
            "outro": "\n\nหากโครงการใดตรงใจเป็นพิเศษ ดิฉันยินดีเป็นอย่างยิ่งที่จะให้ข้อมูลเชิงลึกเพิ่มเติมค่ะ"
            }
             ,
            "casual": {
            "intro": get_empathetic_message(query, properties[0].get("ประเภท", ""), language) + "ลองดูพวกนี้เลย บอกเลยว่าเจอของเด็ดเข้าแล้ว! 😎",
            "property": "\n\n{index}. อันนี้น่าสน! {type} ที่ {project}\n   ราคาน่าโดน: {price} บาท ({status})\n   ทำเลดีเว่อร์: {location}\n   ละแวกนี้ของกิน คาเฟ่ เพียบ! → {nearby}",
            "outro": "\n\nมีอันไหนโดนใจมั้ย? ถ้าชอบ เดี๋ยวเล่าให้ฟังอีกเยอะเลย 😄"
            },
            "friendly": {
            "intro": get_empathetic_message(query, properties[0].get("ประเภท", ""), language) + "มีที่น่าสนใจมากๆ มาแนะนำค่า รีบมาเล่าเลย~ 🥰",
            "property": "\n\n{index}. น่ารักสุดๆ! {type} ที่ {project}\n   ราคาดีต่อใจ: {price} บาท ({status})\n   โลเคชันน่าอยู่มาก: {location}\n   รอบๆ มีครบทุกอย่างเลยน้า: {nearby}",
            "outro": "\n\nถูกใจมั้ยคะ? ถ้าสนใจตัวไหนเป็นพิเศษ บอกมาได้เลยน้า จะเล่าแบบละเอียดยิบให้เลยค่า 💬✨"
            },
            "professional": {
            "intro": get_empathetic_message(query, properties[0].get("ประเภท", ""), language) + "จากการวิเคราะห์รายละเอียดความต้องการของท่าน ผมได้คัดเลือกอสังหาริมทรัพย์ที่มีศักยภาพในการลงทุนตามหัวข้อ '{query}' ไว้ดังนี้ครับ:",
            "property": "\n\n{index}. {type} ระดับพรีเมียม - {project}\n   มูลค่าการลงทุนที่น่าสนใจ: {price} บาท ({status})\n   ทำเลเชิงกลยุทธ์: {location}\n   สิ่งอำนวยความสะดวกครบครัน รองรับทุกไลฟ์สไตล์: {nearby}",
            "outro": "\n\nหากท่านต้องการข้อมูลในเชิงลึกเพิ่มเติมเกี่ยวกับโครงการใด ผมยินดีจัดเตรียมรายละเอียดแบบครบถ้วนให้ครับ"
            }
        }

    template = response_templates.get(consultation_style, response_templates["formal"])
    
    # สร้าง response
    response = template["intro"].format(query=query)
    
    for i, prop in enumerate(properties, 1):
        # แปลงข้อมูลเป็นภาษาอังกฤษถ้าจำเป็น
        if language == "english":
            prop = translate_property_data(prop)
            
        property_text = template["property"].format(
            index=i,
            type=prop.get("type_en" if language == "english" else "ประเภท", ""),
            project=prop.get("project_en" if language == "english" else "โครงการ", ""),
            price=prop.get("price_en" if language == "english" else "ราคา", ""),
            status=prop.get("status_en" if language == "english" else "รูปแบบ", ""),
            location=prop.get("location_en" if language == "english" else "ตำแหน่ง", ""),
            nearby=format_nearby_facilities(prop, language)
        )
        response += property_text
    
    response += template["outro"]
    
    return response

def format_nearby_facilities(property_data: Dict[str, Any], language: str = "thai") -> str:
    """Format nearby facilities in a more engaging way"""
    facilities = []
    
    if language == "english":
        if property_data.get("educational_institution_en") and property_data["educational_institution_en"] not in ["None", "N/A", None]:
            facilities.append(f"Education: {property_data['educational_institution_en']}")
        if property_data.get("bts_mrt_station_en") and property_data["bts_mrt_station_en"] not in ["None", "N/A", None]:
            facilities.append(f"Transit: {property_data['bts_mrt_station_en']}")
        if property_data.get("shopping_mall_en") and property_data["shopping_mall_en"] not in ["None", "N/A", None]:
            facilities.append(f"Shopping: {property_data['shopping_mall_en']}")
        if property_data.get("hospital_en") and property_data["hospital_en"] not in ["None", "N/A", None]:
            facilities.append(f"Healthcare: {property_data['hospital_en']}")
    else:
        if property_data.get("สถานศึกษา") and property_data["สถานศึกษา"] not in ["ไม่มี", "None", "N/A", None]:
            facilities.append(f"สถานศึกษา: {property_data['สถานศึกษา']}")
        if property_data.get("สถานีรถไฟฟ้า") and property_data["สถานีรถไฟฟ้า"] not in ["ไม่มี", "None", "N/A", None]:
            facilities.append(f"รถไฟฟ้า: {property_data['สถานีรถไฟฟ้า']}")
        if property_data.get("ห้างสรรพสินค้า") and property_data["ห้างสรรพสินค้า"] not in ["ไม่มี", "None", "N/A", None]:
            facilities.append(f"ห้างสรรพสินค้า: {property_data['ห้างสรรพสินค้า']}")
        if property_data.get("โรงพยาบาล") and property_data["โรงพยาบาล"] not in ["ไม่มี", "None", "N/A", None]:
            facilities.append(f"โรงพยาบาล: {property_data['โรงพยาบาล']}")
    
    if not facilities:
        return "ไม่มีข้อมูลสิ่งอำนวยความสะดวกใกล้เคียง" if language == "thai" else "No nearby facilities information"
    
    return " | ".join(facilities)

@app.get("/")
async def root():
    return {"message": "AI Property Consultant API is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(query: PropertyQuery):
    try:
        # Generate or retrieve session ID
        session_id = query.session_id
        chat_room_id = query.chat_room_id
        user_id = query.user_id
        
        # ถ้ามี chat_room_id แต่ไม่มี session_id ให้ใช้ chat_room_id เป็น session_id
        if chat_room_id and not session_id:
            session_id = chat_room_id
        
        # ถ้ามี session_id แต่ไม่มี chat_room_id ให้ใช้ session_id เป็น chat_room_id
        if session_id and not chat_room_id:
            chat_room_id = session_id
            
        if not session_id:
            session_id = f"session_{secrets.token_hex(8)}"
            chat_room_id = session_id
            user_sessions[session_id] = {
                "created_at": datetime.now(),
                "queries": []
            }
        elif session_id not in user_sessions:
            user_sessions[session_id] = {
                "created_at": datetime.now(),
                "queries": []
            }
        
        # ถ้าต้องการดึงประวัติการสนทนา
        if query.get_history:
            # ลองดึงจาก MongoDB ก่อน
            chat_room = mongodb_manager.get_chat_room(chat_room_id)
            if chat_room and "messages" in chat_room:
                return ChatResponse(
                    response="",
                    session_id=session_id,
                    chat_room_id=chat_room_id,
                    messages=chat_room["messages"]
                )
            
            # ถ้าไม่มีใน MongoDB ให้ดึงจาก memory
            messages = user_sessions[session_id].get("messages", [])
            return ChatResponse(
                response="",
                session_id=session_id,
                chat_room_id=chat_room_id,
                messages=messages
            )
        
        # Log the query
        user_sessions[session_id]["queries"].append({
            "query": query.query,
            "timestamp": datetime.now()
        })
        
        # Search for relevant properties
        relevant_properties = vector_search(query.query, language=query.language or "thai")
        formatted_properties = format_property_response(relevant_properties)
        
        # Generate AI response
        response = generate_ai_response(
            query.query, 
            formatted_properties, 
            query.consultation_style,
            query.language or "thai"  # ถ้าไม่ระบุภาษาให้ใช้ภาษาไทยเป็นค่าเริ่มต้น
        )
        
        # บันทึกข้อความลงในประวัติการสนทนา
        if query.save_message:
            if "messages" not in user_sessions[session_id]:
                user_sessions[session_id]["messages"] = []
                
            # สร้างข้อความของผู้ใช้
            user_message = {
                "role": "user",
                "content": query.query,
                "timestamp": query.timestamp or int(time.time() * 1000)
            }
            
            # สร้างข้อความของ AI
            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": int(time.time() * 1000),
                "properties": formatted_properties if formatted_properties else None
            }
            
            # บันทึกลง memory
            user_sessions[session_id]["messages"].append(user_message)
            user_sessions[session_id]["messages"].append(assistant_message)
            
            # บันทึกลง MongoDB
            try:
                mongodb_manager.save_chat_room(chat_room_id, [user_message, assistant_message], user_id)
            except Exception as e:
                logger.error(f"Error saving to MongoDB: {str(e)}")
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            chat_room_id=chat_room_id,
            properties=formatted_properties if formatted_properties else None
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), consultation_style: str = "formal"):
    try:
        global property_data
        
        # Validate file type
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['csv', 'xlsx', 'xls']:
            raise HTTPException(status_code=400, detail="Only CSV or Excel files are accepted")
        
        # Read the file content
        content = await file.read()
        
        if file_ext == 'csv':
            df = pd.read_csv(io.BytesIO(content))
        else:  # Excel file
            df = pd.read_excel(io.BytesIO(content))
            
        # Validate expected columns
        expected_columns = [
            'ประเภท', 'โครงการ', 'ราคา', 'รูปแบบ', 'รูป', 'ตำแหน่ง', 
            'สถานศึกษา', 'สถานีรถไฟฟ้า', 'ห้างสรรพสินค้า', 'โรงพยาบาล', 'สนามบิน'
        ]
        
        for col in expected_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Missing required column: {col}"
                )
                
        # Convert DataFrame to list of dicts for our database
        property_data = df.fillna("ไม่มี").to_dict('records')
        
        # Generate a unique file ID
        file_id = f"upload_{secrets.token_hex(8)}"
        
        # บันทึกลง MongoDB
        try:
            mongodb_manager.store_properties(property_data, file_id)
        except Exception as e:
            logger.error(f"Error storing properties in MongoDB: {str(e)}")
        
        return UploadResponse(
            message="อัพโหลดข้อมูลอสังหาริมทรัพย์สำเร็จ",
            file_id=file_id,
            num_records=len(property_data)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error processing file: " + str(e))

@app.post("/api/save_history")
async def save_chat_history(history_request: ChatHistoryRequest):
    try:
        chat_room_id = history_request.chat_room_id
        messages = history_request.messages
        user_id = history_request.user_id
        
        # บันทึกลง MongoDB
        success = mongodb_manager.save_chat_room(chat_room_id, messages, user_id)
        
        if not success:
            # ถ้าบันทึกลง MongoDB ไม่สำเร็จ ให้บันทึกลง memory
            if chat_room_id not in user_sessions:
                user_sessions[chat_room_id] = {
                    "created_at": datetime.now(),
                    "queries": [],
                    "messages": []
                }
            
            # บันทึกข้อความลงในประวัติการสนทนา
            if "messages" not in user_sessions[chat_room_id]:
                user_sessions[chat_room_id]["messages"] = []
                
            # เพิ่มข้อความใหม่
            for message in messages:
                user_sessions[chat_room_id]["messages"].append(message)
        
        return {"success": True, "message": "บันทึกประวัติการสนทนาสำเร็จ"}
        
    except Exception as e:
        logger.error(f"Error saving chat history: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error saving chat history: " + str(e))

@app.get("/api/styles")
async def get_consultation_styles():
    return CONSULTATION_STYLES

# เพิ่ม API endpoint สำหรับการลงทะเบียน
@app.post("/api/register", response_model=UserResponse)
async def register_user(user_data: UserRegisterRequest):
    try:
        # ตรวจสอบว่ามีอีเมลนี้ในระบบแล้วหรือไม่
        existing_user = mongodb_manager.get_user_by_email(user_data.email)
        
        if existing_user:
            return UserResponse(
                id="",
                name="",
                email="",
                success=False,
                message="อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น"
            )
        
        # สร้างผู้ใช้ใหม่
        new_user = {
            "id": f"user_{secrets.token_hex(8)}",
            "name": user_data.name,
            "email": user_data.email,
            "password": user_data.password,  # ในระบบจริงควรเข้ารหัส
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # บันทึกลง MongoDB
        success = mongodb_manager.save_user(new_user)
        
        if success:
            return UserResponse(
                id=new_user["id"],
                name=new_user["name"],
                email=new_user["email"],
                success=True,
                message="ลงทะเบียนสำเร็จ"
            )
        else:
            return UserResponse(
                id="",
                name="",
                email="",
                success=False,
                message="เกิดข้อผิดพลาดในการลงทะเบียน กรุณาลองใหม่อีกครั้ง"
            )
            
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        logger.error(traceback.format_exc())
        return UserResponse(
            id="",
            name="",
            email="",
            success=False,
            message=f"เกิดข้อผิดพลาด: {str(e)}"
        )

# เพิ่ม API endpoint สำหรับการเข้าสู่ระบบ
@app.post("/api/login", response_model=UserResponse)
async def login_user(user_data: UserLoginRequest):
    try:
        # ค้นหาผู้ใช้จากอีเมล
        user = mongodb_manager.get_user_by_email(user_data.email)
        
        if not user:
            return UserResponse(
                id="",
                name="",
                email="",
                success=False,
                message="ไม่พบผู้ใช้นี้ในระบบ"
            )
        
        # ตรวจสอบรหัสผ่าน
        if user["password"] != user_data.password:  # ในระบบจริงควรเปรียบเทียบรหัสผ่านที่เข้ารหัสแล้ว
            return UserResponse(
                id="",
                name="",
                email="",
                success=False,
                message="รหัสผ่านไม่ถูกต้อง"
            )
        
        # เข้าสู่ระบบสำเร็จ
        return UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            success=True,
            message="เข้าสู่ระบบสำเร็จ"
        )
            
    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        logger.error(traceback.format_exc())
        return UserResponse(
            id="",
            name="",
            email="",
            success=False,
            message=f"เกิดข้อผิดพลาด: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
