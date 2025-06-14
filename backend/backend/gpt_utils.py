import openai
import os
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path
import logging

# Basic logging setup just for errors
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Try to load .env from current directory and parent directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent

# Try loading from current directory first
env_path = current_dir / '.env'
if not env_path.exists():
    # Try parent directory
    env_path = parent_dir / '.env'

load_dotenv(env_path, override=True)

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Set up OpenAI client
openai.api_key = api_key

class MessageTemplates:
    """
    Pre-defined message templates
    - Different styles
    - Different tones
    - Different languages
    """
    # Implementation needed

class GPTMessageGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=api_key)
    
    def generate_motivational_message(self, message_type: str) -> str:
        """Generate a motivational message based on the type (meal or workout)"""
        
        prompts = {
            "meal": """
            Generate a short, encouraging SMS message (max 160 characters) to remind someone 
            about eating a healthy meal. Make it motivational, friendly, and actionable.
            Examples: "🍎 Time to fuel your body with nutritious food! Your health goals are within reach!"
            """,
            "workout": """
            Generate a short, encouraging SMS message (max 160 characters) to motivate someone 
            to work out. Make it energetic, inspiring, and actionable.
            Examples: "💪 Your body is capable of amazing things! Time to show it some love with a great workout!"
            """
        }
        
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a supportive health and fitness coach."},
                    {"role": "user", "content": prompts.get(message_type, prompts["workout"])}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating {message_type} message: {str(e)}")
            # Fallback messages if GPT fails
            fallback_messages = {
                "meal": "🍎 Time for a healthy meal! Fuel your body with good nutrition today!",
                "workout": "💪 Time to move your body! Every workout brings you closer to your goals!"
            }
            return fallback_messages.get(message_type, fallback_messages["workout"])
    
    def generate_reply_to_user(self, user_message: str) -> str:
        """Generate a supportive reply to user's message"""
        
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a supportive health and fitness coach. Respond to user messages 
                        with encouragement, practical advice, or motivation. Keep responses under 160 characters 
                        for SMS. Be empathetic and helpful."""
                    },
                    {
                        "role": "user", 
                        "content": f"User said: '{user_message}'. Respond supportively."
                    }
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating reply: {str(e)}")
            return "I hear you! Remember, every small step counts. You've got this! 💪"
        
    def get_user_message_history(self, phone: str) -> list:
        """
        Retrieve user's message history for context
        """
        # Implementation needed

# Global instance
gpt_generator = GPTMessageGenerator()