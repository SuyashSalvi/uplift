# Uplift: A Full-Stack Application for Personal Growth and Well-being

Welcome to Uplift, a comprehensive platform designed to empower individuals on their journey toward personal growth, mindfulness, and overall well-being. This application provides tools and resources to help users track habits, set goals, practice mindfulness, and connect with a supportive community.

<img width="1262" alt="Screenshot 2025-06-14 at 5 33 46 PM" src="https://github.com/user-attachments/assets/97bea4cd-5df3-4022-b718-91001b15a723" />


## ✨ Features

- **Habit Tracking:** Monitor and build positive habits with intuitive tracking and progress visualization.
- **Goal Setting:** Define and achieve personal goals with a structured approach.
- **Mindfulness Exercises:** Access guided meditations and breathing exercises to enhance focus and reduce stress.
- **Community Support:** Connect with like-minded individuals, share progress, and offer encouragement.
- **Personalized Insights:** Gain valuable insights into your well-being journey through data analytics.

## 🚀 Technologies Used

### Frontend

- **Vue.js 3:** A progressive JavaScript framework for building user interfaces.
- **TypeScript:** A typed superset of JavaScript that compiles to plain JavaScript.
- **Vite:** A fast build tool for modern web projects.
- **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

### Backend

- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Celery:** An asynchronous task queue/job queue based on distributed message passing.
- **Redis:** An open-source, in-memory data structure store, used as a database, cache and message broker (often used with Celery).
- **PostgreSQL:** A powerful, open-source object-relational database system.

## ⚙️ Setup Instructions

To get this project up and running on your local machine, follow these steps:

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)
- PostgreSQL (local installation or access to a cloud instance)
- Redis (local installation or access to a cloud instance)
- Node.js (v14 or higher)
- npm (v6 or higher) or Yarn (v1.22 or higher)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/uplift.git
cd uplift
```

### 2. Backend Setup

Navigate to the `backend` directory and create a Python virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt # (You will need to create this file)
```

Create a `.env` file in the `backend` directory and add your environment variables. A `sample.env` might be provided, otherwise create one with:

```
DATABASE_URL=postgresql://user:password@host:port/database_name
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
SECRET_KEY=your_fastapi_secret_key
```

Apply database migrations (if any):

```bash
# Example for Alembic or similar ORM migration tool
# alembic upgrade head
```

### 3. Frontend Setup

Navigate to the `frontend` directory and install dependencies:

```bash
cd ../frontend
npm install
# or
yarn install
```

## ▶️ Running the Application

### 1. Start PostgreSQL and Redis

Ensure your PostgreSQL and Redis servers are running.

### 2. Start the Backend Server

Activate your virtual environment (if not already active) and in the `backend` directory, run:

```bash
uvicorn main:app --reload # Assuming your main FastAPI app is in main.py
```

### 3. Start Celery Worker (Optional, for background tasks)

In the `backend` directory, with the virtual environment active, run:

```bash
celery -A your_celery_app worker -l info # Replace your_celery_app with your Celery instance
```

The backend API will typically run on `http://localhost:8000` (FastAPI default) or the port specified in your configuration.

### 4. Start the Frontend Development Server

In the `frontend` directory, run:

```bash
npm run dev
# or
yarn dev
```

The frontend application will typically open in your browser at `http://localhost:5173` (or another port if 5173 is in use).

## 📁 Project Structure

```
uplift/
├── backend/                # Backend (FastAPI, Celery, Redis, PostgreSQL) services
│   ├── venv/               # Python virtual environment
│   ├── src/
│   ├── database/           # Database setup and migrations
│   ├── schemas/            # Pydantic models for data validation
│   ├── crud/               # CRUD operations
│   ├── api/                # API routes
│   ├── core/               # Core configurations and utilities
│   ├── tasks/              # Celery tasks
│   ├── main.py             # FastAPI application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend (Vue.js, Vite, TypeScript) application
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── views/
│   │   └── App.vue
│   └── package.json
├── .gitignore              # Git ignore file
├── README.md               # Project README (this file)
└── package.json            # (Optional) Monorepo package.json if used
```

## 🤝 Contributing

We welcome contributions to Uplift! Please read our `CONTRIBUTING.md` (to be created) for details on our code of conduct, and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details. 
