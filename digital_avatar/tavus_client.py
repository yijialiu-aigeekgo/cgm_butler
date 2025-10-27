"""
Tavus API Client

This module provides a client for interacting with the Tavus Digital Avatar API.
"""

import requests
from typing import Dict, Optional, Any
import os


class TavusClient:
    """Client for Tavus Digital Avatar API."""
    
    BASE_URL = "https://tavusapi.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavus client.
        
        Args:
            api_key: Tavus API key. If None, reads from environment variable TAVUS_API_KEY
        """
        # 尝试从多个来源获取API key
        self.api_key = api_key or os.getenv('TAVUS_API_KEY')
        
        # 如果还是没有，尝试从config导入
        if not self.api_key:
            try:
                from digital_avatar.config import AvatarConfig
                self.api_key = AvatarConfig.TAVUS_API_KEY
            except:
                pass
        
        if not self.api_key:
            raise ValueError("Tavus API key is required. Set TAVUS_API_KEY environment variable or pass api_key parameter.")
        
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
    
    def update_persona(self, persona_id: str, data: Dict[str, Any]) -> Dict:
        """
        Update a persona's settings.
        
        Args:
            persona_id: The persona ID (e.g., 'p754b367b5f0')
            data: Update data
        
        Returns:
            Response from Tavus API
        """
        url = f"{self.BASE_URL}/v2/personas/{persona_id}"
        
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def get_persona(self, persona_id: str) -> Dict:
        """
        Get persona information.
        
        Args:
            persona_id: The persona ID
        
        Returns:
            Persona information
        """
        url = f"{self.BASE_URL}/v2/personas/{persona_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def create_conversation(self, persona_id: str, config: Dict[str, Any]) -> Dict:
        """
        Create a new conversation with the digital avatar.
        
        Args:
            persona_id: The persona ID
            config: Conversation configuration
        
        Returns:
            Conversation details including session ID
        """
        url = f"{self.BASE_URL}/v2/conversations"
        
        data = {
            "persona_id": persona_id,
            **config
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def send_message(self, conversation_id: str, message: str) -> Dict:
        """
        Send a message in a conversation.
        
        Args:
            conversation_id: The conversation ID
            message: Message text
        
        Returns:
            Response from the avatar
        """
        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}/messages"
        
        data = {
            "message": message
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def get_conversation_history(self, conversation_id: str) -> Dict:
        """
        Get conversation history.
        
        Args:
            conversation_id: The conversation ID
        
        Returns:
            Conversation history
        """
        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def end_conversation(self, conversation_id: str) -> Dict:
        """
        End a conversation.
        
        Args:
            conversation_id: The conversation ID
        
        Returns:
            Response confirming conversation ended
        """
        url = f"{self.BASE_URL}/v2/conversations/{conversation_id}/end"
        
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


if __name__ == '__main__':
    # Example usage
    try:
        client = TavusClient()
        
        # Get persona info
        persona_id = "p754b367b5f0"
        persona = client.get_persona(persona_id)
        print(f"Persona: {persona}")
        
    except Exception as e:
        print(f"Error: {e}")

