# AI-Powered SMS Reminder Backend

A FastAPI backend service that sends AI-generated motivational SMS reminders for meals and workouts using OpenAI GPT-4 and Twilio.

## Features

- **Schedule SMS Reminders**: Users can schedule daily reminders for meals or workouts
- **AI-Generated Messages**: Uses OpenAI GPT-4 to create personalized motivational messages
- **Interactive SMS Replies**: Responds to user messages with AI-generated supportive replies
- **Background Task Processing**: Uses Celery with Redis for reliable message scheduling
- **Database Storage**: SQLAlchemy with PostgreSQL/SQLite for storing schedules and logs

## Setup Instructions

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

Required credentials:
- **Twilio**: Account SID, Auth Token, and Phone Number
- **OpenAI**: API Key for GPT-4 access
- **Redis**: URL for Celery task queue
- **Database**: Connection URL

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up -d
```

This starts:
- Redis (task queue)
- PostgreSQL (database)
- FastAPI backend
- Celery worker (background tasks)
- Celery beat (task scheduler)

### 4. Manual Setup (Alternative)

If running without Docker:

```bash
# Start Redis
redis-server

# Start Celery worker (in separate terminal)
celery -A scheduler.celery_app worker --loglevel=info

# Start Celery beat scheduler (in separate terminal)
celery -A scheduler.celery_app beat --loglevel=info

# Start FastAPI server
uvicorn main:app --reload
```

## API Endpoints

### Schedule a Reminder
```bash
POST /schedule
{
    "phone": "+1234567890",
    "message_type": "meal",  # or "workout"
    "time": "12:00"         # 24-hour format
}
```

### Cancel a Schedule
```bash
DELETE /schedule/{schedule_id}
```

### Get User Schedules
```bash
GET /schedules/{phone}
```

### Twilio Webhook
```bash
POST /webhook/twilio-reply
```

### Health Check
```bash
GET /health
```

## Twilio Webhook Setup

1. In your Twilio Console, configure the webhook URL for incoming messages:
   ```
   https://your-domain.com/webhook/twilio-reply
   ```

2. The webhook will:
   - Receive user SMS replies
   - Generate AI responses using GPT-4
   - Reply automatically with supportive messages

## Database Schema

### ScheduledMessage
- `id`: Primary key
- `phone`: User's phone number
- `message_type`: "meal" or "workout"
- `scheduled_time`: Time in "HH:MM" format
- `created_at`: Timestamp
- `is_active`: Boolean flag
- `task_id`: Celery task identifier

### MessageLog
- `id`: Primary key
- `phone`: Recipient phone number
- `message_type`: Type of message sent
- `message_content`: Actual message content
- `sent_at`: Timestamp
- `status`: Delivery status

### UserReply
- `id`: Primary key
- `phone`: User's phone number
- `incoming_message`: User's message
- `bot_response`: AI-generated response
- `received_at`: Timestamp

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── scheduler.py         # Celery tasks and scheduling logic
├── gpt_utils.py         # OpenAI GPT-4 integration
├── twilio_utils.py      # Twilio SMS service
├── twilio_webhook.py    # Webhook handlers for incoming SMS
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker services configuration
├── Dockerfile          # Docker image configuration
└── .env.example        # Environment variables template
```

## Usage Examples

### Schedule a Meal Reminder
```python
import requests

response = requests.post("http://localhost:8000/schedule", json={
    "phone": "+1234567890",
    "message_type": "meal",
    "time": "12:00"
})
```

### Example Generated Messages
- **Meal**: "🍎 Time to fuel your body with nutritious food! Your health goals are within reach!"
- **Workout**: "💪 Your body is capable of amazing things! Time to show it some love with a great workout!"

## Production Deployment

1. Use environment variables for all sensitive configuration
2. Enable HTTPS for webhook endpoints
3. Configure proper CORS settings
4. Set up monitoring and logging
5. Use a production WSGI server like Gunicorn
6. Configure database connection pooling
7. Set up proper error tracking (e.g., Sentry)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.