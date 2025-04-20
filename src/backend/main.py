
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

# Create models for request/response
class PropertyQuery(BaseModel):
    query: str
    consultation_style: str = "formal"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    properties: Optional[List[Dict[str, Any]]] = None

class UploadResponse(BaseModel):
    message: str
    file_id: str
    num_records: int

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

# Simulated vector search function
def vector_search(query: str, top_k: int = 3):
    """
    Simulate vector search in the property database
    Returns relevant properties based on the query
    """
    if not property_data:
        return []
    
    # In a real implementation, this would use embedding similarity
    # For now, we'll just do a simple keyword match
    keywords = query.lower().split()
    scored_items = []
    
    for item in property_data:
        score = 0
        item_text = json.dumps(item, ensure_ascii=False).lower()
        
        for keyword in keywords:
            if keyword in item_text:
                score += 1
                
        if score > 0:
            scored_items.append((item, score))
    
    # Sort by score and take top_k
    scored_items.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in scored_items[:top_k]]

# Format property response based on missing data
def format_property_response(properties):
    """
    Formats property data by removing fields with value 'ไม่มี'
    """
    formatted = []
    for prop in properties:
        formatted_prop = {}
        for key, value in prop.items():
            if value != "ไม่มี":
                formatted_prop[key] = value
        formatted.append(formatted_prop)
    return formatted

# Generate AI response based on consultation style
def generate_ai_response(query: str, properties: List[Dict[str, Any]], style: str):
    """
    Generate AI response based on the query, matched properties and consultation style
    """
    # This would connect to an LLM in production
    # For now we'll create templated responses
    
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

@app.get("/")
async def root():
    return {"message": "AI Property Consultant API is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(query: PropertyQuery):
    try:
        # Generate or retrieve session ID
        session_id = query.session_id
        if not session_id:
            session_id = f"session_{secrets.token_hex(8)}"
            user_sessions[session_id] = {
                "created_at": datetime.now(),
                "queries": []
            }
        elif session_id not in user_sessions:
            user_sessions[session_id] = {
                "created_at": datetime.now(),
                "queries": []
            }
        
        # Log the query
        user_sessions[session_id]["queries"].append({
            "query": query.query,
            "timestamp": datetime.now()
        })
        
        # Search for relevant properties
        relevant_properties = vector_search(query.query)
        formatted_properties = format_property_response(relevant_properties)
        
        # Generate AI response
        response = generate_ai_response(
            query.query, 
            formatted_properties, 
            query.consultation_style
        )
        
        return ChatResponse(
            response=response,
            session_id=session_id,
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

@app.get("/api/styles")
async def get_consultation_styles():
    return CONSULTATION_STYLES

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
