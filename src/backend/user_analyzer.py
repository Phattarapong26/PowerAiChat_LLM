
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class UserAnalyzer:
    def __init__(self, mongodb_manager=None):
        """
        Analyzes user behavior and preferences
        """
        self.mongodb_manager = mongodb_manager
        logger.info("Initialized UserAnalyzer")
        
    def analyze_user_interests(self, session_id: str) -> Dict[str, Any]:
        """
        Analyze user interests based on chat history
        """
        try:
            if not self.mongodb_manager:
                return {"error": "MongoDB manager not available"}
                
            session = self.mongodb_manager.get_session(session_id)
            if not session:
                return {"error": "Session not found"}
                
            messages = session.get("messages", [])
            if not messages:
                return {"status": "insufficient_data"}
                
            # Extract user queries
            user_queries = [msg["content"] for msg in messages if msg["role"] == "user"]
            
            # Simple keyword analysis (would be more sophisticated in production)
            keywords = {
                "location": ["สุขุมวิท", "รัชดา", "ลาดพร้าว", "รามคำแหง", "อโศก", "ทองหล่อ", "เอกมัย", "บางนา"],
                "property_type": ["คอนโด", "บ้านเดี่ยว", "ทาวน์โฮม", "อพาร์ทเม้นท์", "ที่ดิน", "บ้าน"],
                "price_range": ["ล้าน", "แสน", "ราคา", "งบ", "บาท"],
                "features": ["สระว่ายน้ำ", "ฟิตเนส", "รปภ", "ที่จอดรถ", "ห้องนอน", "ห้องน้ำ", "ตารางวา", "ตารางเมตร"]
            }
            
            interests = {
                "location": [],
                "property_type": [],
                "price_range": [],
                "features": []
            }
            
            for query in user_queries:
                for category, terms in keywords.items():
                    for term in terms:
                        if term in query:
                            if term not in interests[category]:
                                interests[category].append(term)
            
            return {
                "status": "success",
                "interests": interests,
                "query_count": len(user_queries)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing user interests: {str(e)}")
            return {"error": str(e)}
            
    def get_recommendations(self, user_id: Optional[str] = None, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get property recommendations based on user interests
        """
        try:
            # This would connect to a recommendation system in production
            # Here we'll just return mock recommendations
            
            recommendations = [
                {
                    "id": "prop1",
                    "ประเภท": "คอนโด",
                    "โครงการ": "Urban Living",
                    "ราคา": "3,500,000",
                    "รูปแบบ": "ขาย",
                    "reason": "Based on your interest in condos near BTS"
                },
                {
                    "id": "prop2",
                    "ประเภท": "บ้านเดี่ยว",
                    "โครงการ": "Garden Villa",
                    "ราคา": "6,200,000",
                    "รูปแบบ": "ขาย",
                    "reason": "Similar to properties you viewed"
                }
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return []
