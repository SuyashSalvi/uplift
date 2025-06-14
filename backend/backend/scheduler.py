from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models import get_db, ScheduledMessage, MessageLog
from gpt_utils import gpt_generator
from twilio_utils import twilio_service

load_dotenv()

# Initialize Celery
celery_app = Celery(
    'sms_scheduler',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0')
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def send_scheduled_message(phone: str, message_type: str, schedule_id: int):
    """Background task to send scheduled SMS message"""
    
    # Generate motivational message using GPT
    message_content = gpt_generator.generate_motivational_message(message_type)
    
    # Send SMS via Twilio
    result = twilio_service.send_sms(phone, message_content)
    
    # Log the message
    db = next(get_db())
    try:
        message_log = MessageLog(
            phone=phone,
            message_type=message_type,
            message_content=message_content,
            status="sent" if result["success"] else "failed"
        )
        db.add(message_log)
        db.commit()
        
        return {
            "success": result["success"],
            "message": message_content,
            "twilio_result": result
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@celery_app.task
def schedule_daily_message(phone: str, message_type: str, time_str: str, schedule_id: int):
    """Schedule a message to be sent daily at a specific time"""
    
    # Parse the time string (HH:MM)
    try:
        hour, minute = map(int, time_str.split(':'))
    except ValueError:
        return {"success": False, "error": "Invalid time format"}
    
    # Schedule the task to run daily at the specified time
    celery_app.conf.beat_schedule[f'daily_reminder_{schedule_id}'] = {
        'task': 'scheduler.send_scheduled_message',
        'schedule': crontab(hour=hour, minute=minute),
        'args': (phone, message_type, schedule_id)
    }
    
    return {"success": True, "message": f"Scheduled daily reminder at {time_str}"}

def create_schedule(phone: str, message_type: str, time_str: str) -> dict:
    """Create a new scheduled message entry"""
    
    db = next(get_db())
    try:
        # Create database entry
        schedule = ScheduledMessage(
            phone=phone,
            message_type=message_type,
            scheduled_time=time_str
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        
        # Schedule the Celery task
        task = schedule_daily_message.delay(phone, message_type, time_str, schedule.id)
        
        # Update the schedule with task ID
        schedule.task_id = task.id
        db.commit()
        
        return {
            "success": True,
            "schedule_id": schedule.id,
            "task_id": task.id,
            "message": f"Scheduled {message_type} reminder for {time_str}"
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

def cancel_schedule(schedule_id: int) -> dict:
    """Cancel a scheduled message"""
    
    db = next(get_db())
    try:
        schedule = db.query(ScheduledMessage).filter(ScheduledMessage.id == schedule_id).first()
        if not schedule:
            return {"success": False, "error": "Schedule not found"}
        
        # Cancel the Celery task
        if schedule.task_id:
            celery_app.control.revoke(schedule.task_id, terminate=True)
        
        # Deactivate the schedule
        schedule.is_active = False
        db.commit()
        
        return {"success": True, "message": "Schedule cancelled"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()