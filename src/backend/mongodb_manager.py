import logging
from typing import Dict, List, Any, Optional
from pymongo import MongoClient
import pandas as pd
from config import MONGODB_URL, MONGODB_DB

logger = logging.getLogger(__name__)

class MongoDBManager:
    def __init__(self):
        try:
            self.client = MongoClient(MONGODB_URL)
            self.db = self.client[MONGODB_DB]
            self.properties = self.db["properties"]
            self.sessions = self.db["sessions"]
            self.users = self.db["users"]
            self.uploads = self.db["uploads"]
            self.chat_rooms = self.db["chat_rooms"]
            logger.info(f"Connected to MongoDB at {MONGODB_URL}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def store_properties(self, properties: List[Dict[str, Any]], file_id: str) -> str:
        """
        Store property data from uploaded file
        """
        try:
            # Add file_id to each property
            for prop in properties:
                prop["file_id"] = file_id
            
            # Insert properties
            result = self.properties.insert_many(properties)
            return str(result.inserted_ids)
        except Exception as e:
            logger.error(f"Error storing properties: {str(e)}")
            raise

    def get_properties(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Retrieve properties based on query
        """
        try:
            if query is None:
                query = {}
            return list(self.properties.find(query, {"_id": 0}))
        except Exception as e:
            logger.error(f"Error retrieving properties: {str(e)}")
            raise

    def create_session(self, session_id: str, user_id: Optional[str] = None) -> str:
        """
        Create a new chat session
        """
        try:
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": pd.Timestamp.now(),
                "messages": []
            }
            self.sessions.insert_one(session_data)
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise

    def add_message(self, session_id: str, message: Dict[str, Any]) -> bool:
        """
        Add a message to an existing session
        """
        try:
            result = self.sessions.update_one(
                {"session_id": session_id},
                {"$push": {"messages": message}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            raise

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Retrieve a chat session
        """
        try:
            return self.sessions.find_one({"session_id": session_id}, {"_id": 0})
        except Exception as e:
            logger.error(f"Error retrieving session: {str(e)}")
            raise

    def save_chat_room(self, chat_room_id: str, messages: List[Dict[str, Any]], user_id: Optional[str] = None) -> bool:
        """
        บันทึกหรืออัปเดตห้องแชทใน MongoDB
        
        Args:
            chat_room_id: รหัสห้องแชท
            messages: ข้อความในห้องแชท
            user_id: รหัสผู้ใช้ (ถ้ามี)
            
        Returns:
            bool: True ถ้าบันทึกสำเร็จ, False ถ้าไม่สำเร็จ
        """
        try:
            # ตรวจสอบว่ามีห้องแชทนี้อยู่แล้วหรือไม่
            existing_room = self.chat_rooms.find_one({"chat_room_id": chat_room_id})
            
            if existing_room:
                # อัปเดตห้องแชทที่มีอยู่
                result = self.chat_rooms.update_one(
                    {"chat_room_id": chat_room_id},
                    {
                        "$set": {
                            "updated_at": pd.Timestamp.now(),
                            "last_message": messages[-1] if messages else None
                        },
                        "$push": {"messages": {"$each": messages}}
                    }
                )
                return result.modified_count > 0
            else:
                # สร้างห้องแชทใหม่
                chat_room_data = {
                    "chat_room_id": chat_room_id,
                    "user_id": user_id,
                    "created_at": pd.Timestamp.now(),
                    "updated_at": pd.Timestamp.now(),
                    "messages": messages,
                    "last_message": messages[-1] if messages else None
                }
                self.chat_rooms.insert_one(chat_room_data)
                return True
        except Exception as e:
            logger.error(f"Error saving chat room: {str(e)}")
            return False
            
    def get_chat_room(self, chat_room_id: str) -> Dict[str, Any]:
        """
        ดึงข้อมูลห้องแชทจาก MongoDB
        
        Args:
            chat_room_id: รหัสห้องแชท
            
        Returns:
            Dict[str, Any]: ข้อมูลห้องแชท หรือ None ถ้าไม่พบ
        """
        try:
            return self.chat_rooms.find_one({"chat_room_id": chat_room_id}, {"_id": 0})
        except Exception as e:
            logger.error(f"Error retrieving chat room: {str(e)}")
            return None
            
    def get_user_chat_rooms(self, user_id: str) -> List[Dict[str, Any]]:
        """
        ดึงรายการห้องแชทของผู้ใช้
        
        Args:
            user_id: รหัสผู้ใช้
            
        Returns:
            List[Dict[str, Any]]: รายการห้องแชท
        """
        try:
            return list(self.chat_rooms.find({"user_id": user_id}, {"_id": 0}))
        except Exception as e:
            logger.error(f"Error retrieving user chat rooms: {str(e)}")
            return []

    def save_user(self, user_data: Dict[str, Any]) -> bool:
        """
        บันทึกหรืออัปเดตข้อมูลผู้ใช้ใน MongoDB
        
        Args:
            user_data: ข้อมูลผู้ใช้ (id, email, name, password)
            
        Returns:
            bool: True ถ้าบันทึกสำเร็จ, False ถ้าไม่สำเร็จ
        """
        try:
            # ตรวจสอบว่ามีผู้ใช้นี้อยู่แล้วหรือไม่
            existing_user = self.users.find_one({"id": user_data["id"]})
            
            if existing_user:
                # อัปเดตข้อมูลผู้ใช้ที่มีอยู่
                result = self.users.update_one(
                    {"id": user_data["id"]},
                    {
                        "$set": {
                            "email": user_data["email"],
                            "name": user_data["name"],
                            "password": user_data["password"],
                            "updated_at": pd.Timestamp.now()
                        }
                    }
                )
                return result.modified_count > 0
            else:
                # สร้างผู้ใช้ใหม่
                user_data["created_at"] = pd.Timestamp.now()
                user_data["updated_at"] = pd.Timestamp.now()
                self.users.insert_one(user_data)
                return True
        except Exception as e:
            logger.error(f"Error saving user: {str(e)}")
            return False
            
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        ดึงข้อมูลผู้ใช้จาก MongoDB
        
        Args:
            user_id: รหัสผู้ใช้
            
        Returns:
            Dict[str, Any]: ข้อมูลผู้ใช้ หรือ None ถ้าไม่พบ
        """
        try:
            return self.users.find_one({"id": user_id}, {"_id": 0})
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            return None
            
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """
        ดึงข้อมูลผู้ใช้จาก MongoDB ด้วยอีเมล
        
        Args:
            email: อีเมลของผู้ใช้
            
        Returns:
            Dict[str, Any]: ข้อมูลผู้ใช้ หรือ None ถ้าไม่พบ
        """
        try:
            return self.users.find_one({"email": email}, {"_id": 0})
        except Exception as e:
            logger.error(f"Error retrieving user by email: {str(e)}")
            return None

    def close(self):
        """
        Close the MongoDB connection
        """
        if hasattr(self, 'client'):
            self.client.close()
