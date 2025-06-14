from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from models import get_db, UserReply
from gpt_utils import gpt_generator
from twilio_utils import twilio_service
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/twilio-reply")
async def handle_twilio_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle incoming SMS messages from Twilio webhook"""
    
    try:
        # Clean up the phone number
        user_phone = From
        user_message = Body.strip()
        
        # Generate AI response using GPT
        bot_response = gpt_generator.generate_reply_to_user(user_message)
        
        # Log the conversation
        reply_log = UserReply(
            phone=user_phone,
            incoming_message=user_message,
            bot_response=bot_response
        )
        db.add(reply_log)
        db.commit()
        
        # Create Twilio response
        twiml_response = MessagingResponse()
        twiml_response.message(bot_response)
        
        return twiml_response
        
    except Exception as e:
        # Log error and send generic response
        twiml_response = MessagingResponse()
        twiml_response.message("Thanks for your message! I'm here to support your health journey. 💪")
        return twiml_response

@router.get("/webhook-test")
async def test_webhook():
    """Test endpoint to verify webhook is working"""
    return {"message": "Twilio webhook is working!", "status": "active"}