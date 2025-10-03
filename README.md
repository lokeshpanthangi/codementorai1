# 🎯 CodeMentor AIME

A modern LeetCode-style coding platform with AI-powered hints and real-time code execution.

## 🚀 Tech Stack

### Frontend
- **React 18** + **TypeScript**
- **Vite** - Fast build tool
- **Tailwind CSS** + **shadcn/ui** - Modern UI components
- **Monaco Editor** - VS Code-like code editor
- **Axios** - API communication

### Backend
- **FastAPI** - High-performance Python API framework
- **MongoDB Atlas** - Cloud database
- **Motor** - Async MongoDB driver
- **Judge0 CE** - Code execution engine (Docker)
- **JWT** - Authentication

## 📦 Project Structure

```
codementorai1/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── main.py         # App entry point
│   │   ├── models.py       # Pydantic models
│   │   ├── database.py     # MongoDB connection
│   │   ├── auth.py         # JWT authentication
│   │   └── config.py       # Environment settings
│   ├── comprehensive_seed.py  # Database seeding script
│   ├── start.ps1           # Windows startup script
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
├── src/                    # React frontend
│   ├── pages/              # Page components
│   ├── components/         # Reusable components
│   ├── services/           # API service layer
│   └── lib/                # Utilities
├── public/                 # Static assets
└── docker-compose.yml      # Judge0 setup
```

## 🛠️ Setup & Installation

### Prerequisites
- Node.js 18+ & npm
- Python 3.11+
- Docker Desktop (for Judge0)
- MongoDB Atlas account

### 1. Clone Repository
```bash
git clone <repository-url>
cd codementorai1
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend runs on: http://localhost:8080

### 3. Backend Setup
```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure .env file
# Update MONGODB_URL with your MongoDB Atlas connection string
# Update SECRET_KEY for JWT

# Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Backend runs on: http://localhost:8000
API docs: http://localhost:8000/docs

### 4. Judge0 Setup (Code Execution)
```bash
# Start Judge0 with Docker
docker-compose up -d

# Verify Judge0 is running
curl http://localhost:2358/about
```

### 5. Seed Database
```bash
cd backend
python comprehensive_seed.py
```

This creates:
- 8 categories (Array, String, Hash Table, DP, Tree, Graph, Linked List, Binary Search)
- 5 sample problems (Two Sum, Valid Parentheses, etc.)
- 10 test cases (3 visible + 2 hidden per problem)
- 1 demo user (email: demo@codementor.ai, password: demo123)
- 1 daily challenge

## 🎮 Features

### ✅ Completed
- **Problem Solving Interface**: Monaco editor with 13 languages
- **Real-time Code Execution**: Run & Submit with Judge0
- **Problem Management**: Browse, filter, search problems
- **Daily Challenges**: New problem every day
- **Category System**: Browse by topics
- **User Authentication**: JWT-based signup/login
- **Test Cases**: Visible (Run) and hidden (Submit) test cases
- **API Integration**: Complete frontend-backend connectivity

### 🚧 In Progress
- Authentication Context & Protected Routes
- User Profile & Statistics
- Submission History
- AI-Powered Hints

## 🔑 Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=codementor
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JUDGE0_API_URL=http://localhost:2358
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 📡 API Endpoints

### Problems
- `GET /problems` - List all problems
- `GET /problems/{slug}` - Get problem details
- `GET /problems/{id}/stats` - Get problem statistics

### Test Cases
- `GET /testcases/{problem_number}/visible` - Visible test cases
- `GET /testcases/{problem_number}/hidden` - Hidden test cases
- `GET /testcases/{problem_number}/all` - All test cases

### Submissions
- `POST /submissions/run` - Run code (visible test cases)
- `POST /submissions/submit` - Submit code (all test cases)
- `GET /submissions/user/{user_id}` - User's submissions

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Categories & Challenges
- `GET /categories` - List all categories
- `GET /categories/{slug}` - Get category details
- `GET /daily-challenge/today` - Today's challenge
- `GET /daily-challenge/history` - Past challenges

## 🎯 Default Credentials

**Demo User:**
- Email: demo@codementor.ai
- Password: demo123

## 🐛 Common Issues

### CORS Errors
- Ensure backend is running on port 8000
- Check ALLOWED_ORIGINS in backend/.env includes frontend URL

### Judge0 Not Working
- Run `docker-compose up -d` in project root
- Check Docker Desktop is running
- Verify: `curl http://localhost:2358/about`

### Database Connection Errors
- Verify MongoDB Atlas connection string in .env
- Check IP whitelist in MongoDB Atlas (allow 0.0.0.0/0 for development)
- Ensure database name is "codementor"

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Judge0 Documentation](https://github.com/judge0/judge0)
- [shadcn/ui Components](https://ui.shadcn.com/)

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ by CodeMentor AI Team**
