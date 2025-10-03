from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth_routes, problem_routes, testcase_routes, submission_routes

# Create FastAPI app
app = FastAPI(
    title="CodeMentor AI Backend",
    description="Backend API for CodeMentor AI - LeetCode-style coding platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    await connect_to_mongo()
    print("🚀 FastAPI server started!")

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()
    print("👋 FastAPI server stopped!")

# Include routers
app.include_router(auth_routes.router)
app.include_router(problem_routes.router)
app.include_router(testcase_routes.router)
app.include_router(submission_routes.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to CodeMentor AI Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "judge0_status": "Check Judge0 at http://localhost:2358/about"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "judge0": f"{settings.JUDGE0_API_URL}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
