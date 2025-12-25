"""
LLM Client for Career Scientist
Uses Google Gemini API for intelligent features
"""
import google.generativeai as genai
import os
import json
from typing import Dict, List, Optional

class LLMClient:
    """
    Wrapper for Gemini API calls
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key. If None, reads from env var GEMINI_API_KEY
        """
        key = api_key or os.getenv("GEMINI_API_KEY", "keyapi")
        
        if key == "keyapi":
            print("[WARNING] Using placeholder API key. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate(self, prompt: str, json_response: bool = False) -> str:
        """
        Generate content using Gemini
        
        Args:
            prompt: Input prompt
            json_response: If True, expects JSON output
            
        Returns:
            Generated text or JSON string
        """
        try:
            if json_response:
                # Configure for JSON output
                generation_config = {
                    "response_mime_type": "application/json"
                }
                response = self.model.generate_content(prompt, generation_config=generation_config)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            print(f"[LLM Error] {e}")
            if "keyapi" in str(e) or "API_KEY" in str(e):
                return json.dumps({"error": "API key not configured"}) if json_response else "Error: API key not set"
            raise
    
    def parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON response, with error handling
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                return json.loads(response[start:end].strip())
            raise
