
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import json
import os
from config import MODEL_CONFIG, VECTOR_SIMILARITY_THRESHOLD, MAX_RESULTS

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embedding_model_name: str = None):
        """
        Initialize vector store for property data
        
        In a production environment, this would use a proper vector database
        or embedding model. For this demonstration, we're implementing a
        simplified version.
        """
        self.embedding_model_name = embedding_model_name or MODEL_CONFIG['embedding_model']
        self.vectors = []
        self.property_data = []
        logger.info(f"Initialized VectorStore with model: {self.embedding_model_name}")
        
    def add_properties(self, properties: List[Dict[str, Any]]) -> None:
        """
        Add properties to the vector store
        """
        try:
            # In production, this would calculate actual embeddings
            # For demonstration, we'll just store the property data
            self.property_data.extend(properties)
            
            # Create simple mock "embeddings" by concatenating key property values
            for prop in properties:
                text_representation = self._get_property_text(prop)
                mock_embedding = self._mock_embedding(text_representation)
                self.vectors.append(mock_embedding)
                
            logger.info(f"Added {len(properties)} properties to vector store")
        except Exception as e:
            logger.error(f"Error adding properties to vector store: {str(e)}")
            raise
            
    def _get_property_text(self, prop: Dict[str, Any]) -> str:
        """
        Convert property data to text for embedding
        """
        relevant_fields = [
            'ประเภท', 'โครงการ', 'รูปแบบ', 'ตำแหน่ง', 'สถานศึกษา', 
            'สถานีรถไฟฟ้า', 'ห้างสรรพสินค้า', 'โรงพยาบาล', 'สนามบิน'
        ]
        
        text_parts = []
        for field in relevant_fields:
            if field in prop and prop[field] != "ไม่มี":
                text_parts.append(str(prop[field]))
                
        return " ".join(text_parts)
        
    def _mock_embedding(self, text: str) -> np.ndarray:
        """
        Create a mock embedding for demo purposes
        In production, this would use an actual embedding model
        """
        # Create a simple deterministic "embedding" based on the text
        # This is NOT a real embedding, just for demonstration
        import hashlib
        
        # Generate a hash of the text
        hash_object = hashlib.md5(text.encode())
        hash_hex = hash_object.hexdigest()
        
        # Convert the hash to a fake embedding vector (32 dimensions)
        mock_vector = np.array([int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, 32, 2)])
        return mock_vector
        
    def search(self, query: str, top_k: int = MAX_RESULTS) -> List[Dict[str, Any]]:
        """
        Search for properties similar to the query
        """
        try:
            if not self.vectors or not self.property_data:
                logger.warning("Vector store is empty")
                return []
                
            # Create query embedding
            query_embedding = self._mock_embedding(query)
            
            # Calculate similarities
            similarities = []
            for i, vec in enumerate(self.vectors):
                # Cosine similarity
                similarity = np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec))
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
