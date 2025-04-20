
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

    def close(self):
        """
        Close the MongoDB connection
        """
        if hasattr(self, 'client'):
            self.client.close()
