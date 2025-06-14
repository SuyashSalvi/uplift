from twilio.rest import Client
import os
from dotenv import load_dotenv
from typing import Optional

# Force reload environment variables
load_dotenv(override=True)

class TwilioService:
    def __init__(self):
        # Get environment variables
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        
        # Debug logging
        print("\n=== Twilio Configuration ===")
        print(f"Account SID: {self.account_sid}")
        print(f"Auth Token: {self.auth_token}")
        print(f"Phone Number: {self.phone_number}")
        print("==========================\n")
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Missing required Twilio environment variables")
            
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_sms(self, to_phone: str, message: str) -> dict:
        """Send SMS message via Twilio"""
        try:
            print(f"Attempting to send SMS to {to_phone} with message: {message}")
            print(f"Using Twilio credentials - Account SID: {self.account_sid[:6]}..., Auth Token: {self.auth_token[:6]}..., Phone: {self.phone_number}")
            
            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_phone
            )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    
    def validate_phone_number(self, phone: str) -> bool:
        """Basic phone number validation"""
        # Remove any non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Should have 10-15 digits (international format)
        return 10 <= len(digits_only) <= 15
    
    def format_phone_number(self, phone: str) -> str:
        """Format phone number for Twilio (ensure it starts with +)"""
        if not phone.startswith('+'):
            # Assume US number if no country code
            if len(phone) == 10:
                phone = '+1' + phone
            else:
                phone = '+' + phone
        return phone

# Global instance
twilio_service = TwilioService()