import logging
from typing import List, Dict, Any, Optional
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
from config import MODEL_CONFIG, VECTOR_SIMILARITY_THRESHOLD, MAX_RESULTS

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embedding_model_name: str = None):
        """
        Initialize vector store for property data using Sentence Transformers
        """
        self.embedding_model_name = embedding_model_name or MODEL_CONFIG['embedding_model']
        self.model = SentenceTransformer(self.embedding_model_name)
        self.vectors = []
        self.property_data = []
        logger.info(f"Initialized VectorStore with model: {self.embedding_model_name}")
        
    def add_properties(self, properties: List[Dict[str, Any]]) -> None:
        """
        Add properties to the vector store
        """
        try:
            # Store the property data
            self.property_data.extend(properties)
            
            # Create text representations for embedding
            texts = [self._get_property_text(prop) for prop in properties]
            
            # Generate real embeddings using Sentence Transformers
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            self.vectors.extend(embeddings)
                
            logger.info(f"Added {len(properties)} properties to vector store")
        except Exception as e:
            logger.error(f"Error adding properties to vector store: {str(e)}")
            raise
            
    def _get_property_text(self, prop: Dict[str, Any]) -> str:
        """
        Convert property data to text for embedding with weighted importance
        """
        # กำหนดน้ำหนักให้กับแต่ละฟิลด์
        weighted_fields = {
            'ประเภท': 3,  # ให้ความสำคัญสูงสุดกับประเภท
            'ตำแหน่ง': 2,  # ให้ความสำคัญรองลงมาที่ตำแหน่ง
            'โครงการ': 1,
            'รูปแบบ': 1,
            'สถานศึกษา': 1,
            'สถานีรถไฟฟ้า': 1,
            'ห้างสรรพสินค้า': 1,
            'โรงพยาบาล': 1,
            'สนามบิน': 1
        }
        
        # ประเภทอสังหาริมทรัพย์ที่ถูกต้อง
        valid_property_types = [
            'กิจการ', 'คอนโด', 'ทาวน์โฮม', 'ที่ดิน',
            'บ้าน', 'ร้านค้า', 'สำนักงาน', 'โฮมออฟฟิศ'
        ]
        
        text_parts = []
        for field, weight in weighted_fields.items():
            if field in prop and prop[field] != "ไม่มี":
                # ถ้าเป็นฟิลด์ประเภท ให้ตรวจสอบความถูกต้อง
                if field == 'ประเภท':
                    if prop[field] in valid_property_types:
                        # เพิ่มน้ำหนักให้กับประเภทที่ถูกต้อง
                        text_parts.extend([str(prop[field])] * weight)
                else:
                    # เพิ่มน้ำหนักให้กับฟิลด์อื่นๆ
                    text_parts.extend([str(prop[field])] * weight)
                
        return " ".join(text_parts)
        
    def _extract_location(self, query: str) -> str:
        """
        แยกตำแหน่งจากประโยคค้นหา
        """
        # ตำแหน่งที่พบบ่อย
        common_locations = [
            'บางนา', 'สุขุมวิท', 'รัชดา', 'ลาดพร้าว', 'พระราม 9',
            'สีลม', 'สาทร', 'ทองหล่อ', 'เอกมัย', 'อโศก',
            'ราชดำริ', 'พร้อมพงษ์', 'ทองหล่อ', 'อ่อนนุช', 'บางกะปิ',
            'ลาดกระบัง', 'มีนบุรี', 'บางแค', 'บางบอน', 'บางขุนเทียน'
        ]
        
        # แยกคำจากประโยค
        words = query.split()
        
        # หาตำแหน่งที่ตรงกับตำแหน่งที่พบบ่อย
        for word in words:
            if word in common_locations:
                return word
                
        return ""

    def _extract_property_type(self, query: str) -> str:
        """
        แยกประเภทอสังหาริมทรัพย์จากประโยคค้นหา
        """
        # ประเภทอสังหาริมทรัพย์และคำที่เกี่ยวข้อง
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
        
        # แปลงประโยคเป็นตัวพิมพ์เล็ก
        query_lower = query.lower()
        
        # ตรวจสอบแต่ละประเภท
        for prop_type, keywords in property_types.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return prop_type
                    
        return ""

    def search(self, query: str, top_k: int = MAX_RESULTS) -> List[Dict[str, Any]]:
        """
        Search for properties similar to the query using real vector embeddings
        """
        try:
            if not self.vectors or not self.property_data:
                logger.warning("Vector store is empty")
                return []
                
            # แยกตำแหน่งและประเภทจากประโยคค้นหา
            target_location = self._extract_location(query)
            target_property_type = self._extract_property_type(query)
            
            # Create query embedding using the model
            query_embedding = self.model.encode(query, convert_to_numpy=True)
            
            # Calculate similarities with property type and location boost
            similarities = []
            for i, vec in enumerate(self.vectors):
                # Cosine similarity
                similarity = np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec))
                
                prop = self.property_data[i]
                
                # เพิ่มคะแนนให้กับประเภทที่ตรงกับคำค้นหา
                if 'ประเภท' in prop:
                    if target_property_type and prop['ประเภท'] == target_property_type:
                        similarity *= 2.5  # เพิ่มน้ำหนักให้กับประเภทที่ตรงกัน
                    elif prop['ประเภท'] in query:
                        similarity *= 1.5  # เพิ่มน้ำหนักให้กับประเภทที่อยู่ในคำค้นหา
                
                # เพิ่มคะแนนให้กับตำแหน่งที่ตรงกับคำค้นหา
                if 'ตำแหน่ง' in prop:
                    if target_location and target_location in prop['ตำแหน่ง']:
                        similarity *= 2.0  # เพิ่มน้ำหนักให้กับตำแหน่งที่ตรงกัน
                    elif prop['ตำแหน่ง'] in query:
                        similarity *= 2.3  # เพิ่มน้ำหนักให้กับตำแหน่งที่อยู่ในคำค้นหา
                
                similarities.append((i, similarity))
                
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Filter by threshold and take top_k
            results = []
            for idx, sim in similarities[:top_k]:
                if sim >= VECTOR_SIMILARITY_THRESHOLD:
                    result = self.property_data[idx].copy()
                    result["similarity_score"] = float(sim)
                    results.append(result)
                    
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
