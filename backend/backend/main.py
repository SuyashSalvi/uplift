from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path="/Volumes/T7/projects/uplift/backend/backend/.env")

# Import our modules
from models import create_tables, get_db, ScheduledMessage
from scheduler import create_schedule, cancel_schedule
from twilio_webhook import router as webhook_router
from twilio_utils import twilio_service



# Create FastAPI app
app = FastAPI(
    title="AI-Powered SMS Reminder API",
    description="Schedule motivational SMS reminders powered by AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhook router
app.include_router(webhook_router, prefix="/webhook", tags=["webhooks"])

# Pydantic models for request/response
class ScheduleRequest(BaseModel):
    phone: str
    message_type: str  # "meal" or "workout"
    time: str  # "HH:MM" format

class ScheduleResponse(BaseModel):
    success: bool
    message: str
    schedule_id: int = None
    error: str = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    version: str

class TestSMSRequest(BaseModel):
    phone: str
    message: str

# Initialize database tables
@app.on_event("startup")
async def startup_event():
    create_tables()

# Health check endpoint
@app.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

# Main scheduling endpoint
@app.post("/schedule", response_model=ScheduleResponse)
async def schedule_reminder(
    request: ScheduleRequest,
    db: Session = Depends(get_db)
):
    """Schedule a new SMS reminder"""
    
    # Validate message type
    if request.message_type not in ["meal", "workout"]:
        raise HTTPException(
            status_code=400,
            detail="message_type must be either 'meal' or 'workout'"
        )
    
    # Validate time format
    try:
        time_parts = request.time.split(":")
        if len(time_parts) != 2:
            raise ValueError("Invalid format")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            raise ValueError("Invalid time range")
            
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="time must be in HH:MM format (24-hour)"
        )
    
    # Validate and format phone number
    if not twilio_service.validate_phone_number(request.phone):
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number format"
        )
    
    formatted_phone = twilio_service.format_phone_number(request.phone)
    
    # Create the schedule
    result = create_schedule(
        phone=formatted_phone,
        message_type=request.message_type,
        time_str=request.time
    )
    
    if result["success"]:
        return ScheduleResponse(
            success=True,
            message=result["message"],
            schedule_id=result["schedule_id"]
        )
    else:
        raise HTTPException(status_code=500, detail=result["error"])

# Cancel schedule endpoint
@app.delete("/schedule/{schedule_id}")
async def cancel_reminder(schedule_id: int, db: Session = Depends(get_db)):
    """Cancel a scheduled reminder"""
    
    result = cancel_schedule(schedule_id)
    
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

# List user's schedules
@app.get("/schedules/{phone}")
async def get_user_schedules(phone: str, db: Session = Depends(get_db)):
    """Get all active schedules for a phone number"""
    
    formatted_phone = twilio_service.format_phone_number(phone)
    
    schedules = db.query(ScheduledMessage).filter(
        ScheduledMessage.phone == formatted_phone,
        ScheduledMessage.is_active == True
    ).all()
    
    return {
        "phone": formatted_phone,
        "schedules": [
            {
                "id": schedule.id,
                "message_type": schedule.message_type,
                "scheduled_time": schedule.scheduled_time,
                "created_at": schedule.created_at.isoformat()
            }
            for schedule in schedules
        ]
    }

# Test SMS endpoint (for development)
@app.post("/test-sms")
async def test_sms(request: TestSMSRequest):
    """Test endpoint to send SMS (development only)"""
    
    if not twilio_service.validate_phone_number(request.phone):
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    formatted_phone = twilio_service.format_phone_number(request.phone)
    result = twilio_service.send_sms(formatted_phone, request.message)
    
    if result["success"]:
        return {"message": "SMS sent successfully", "details": result}
    else:
        raise HTTPException(status_code=500, detail=result["error"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )