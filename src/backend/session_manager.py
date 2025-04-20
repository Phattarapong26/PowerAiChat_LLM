
import logging
from typing import Dict, List, Any, Optional
import secrets
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, mongodb_manager=None):
        """
        Manages chat sessions for the AI property consultant
        """
        self.sessions = {}  # In-memory sessions (would use MongoDB in production)
        self.mongodb_manager = mongodb_manager
        logger.info("Initialized SessionManager")
        
    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        Create a new chat session
        """
        try:
            session_id = f"session_{secrets.token_hex(8)}"
            timestamp = datetime.now()
            
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": timestamp,
                "last_activity": timestamp,
                "messages": []
            }
            
            # Store in memory
            self.sessions[session_id] = session_data
            
            # Store in MongoDB if available
            if self.mongodb_manager:
                self.mongodb_manager.create_session(session_id, user_id)
                
            logger.info(f"Created new session: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise
            
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by ID
        """
        # Try in-memory first
        if session_id in self.sessions:
            return self.sessions[session_id]
            
        # Try MongoDB if available
        if self.mongodb_manager:
            return self.mongodb_manager.get_session(session_id)
            
        return None
        
    def add_message(self, session_id: str, role: str, content: str) -> bool:
        """
        Add a message to a session
        """
        try:
            session = self.get_session(session_id)
            if not session:
                logger.warning(f"Session not found: {session_id}")
                return False
                
            timestamp = datetime.now()
            message = {
                "role": role,
                "content": content,
                "timestamp": timestamp
            }
            
            # Update in-memory
            if session_id in self.sessions:
                self.sessions[session_id]["messages"].append(message)
                self.sessions[session_id]["last_activity"] = timestamp
                
            # Update in MongoDB if available
            if self.mongodb_manager:
                self.mongodb_manager.add_message(session_id, message)
                
            return True
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return False
            
    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all messages in a session
        """
        session = self.get_session(session_id)
        if not session:
            return []
            
        return session.get("messages", [])
        
    def clean_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Remove sessions older than max_age_hours
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        count = 0
        
        # Clean in-memory sessions
        session_ids = list(self.sessions.keys())
        for session_id in session_ids:
            last_activity = self.sessions[session_id].get("last_activity")
            if last_activity and last_activity < cutoff_time:
                del self.sessions[session_id]
                count += 1
                
        logger.info(f"Cleaned {count} old sessions")
        return count
