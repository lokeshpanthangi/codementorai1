from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()

async def get_database():
    return db.client[settings.DATABASE_NAME]

async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"✅ Connected to MongoDB at {settings.MONGODB_URL}")
    
async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    db.client.close()
    print("❌ Closed MongoDB connection")

# Collection getters
async def get_users_collection():
    database = await get_database()
    return database.users

async def get_problems_collection():
    database = await get_database()
    return database.problems

async def get_testcases_collection():
    database = await get_database()
    return database.testcases

async def get_submissions_collection():
    database = await get_database()
    return database.submissions

async def get_user_progress_collection():
    database = await get_database()
    return database.userprogress

async def get_categories_collection():
    database = await get_database()
    return database.categories

async def get_ai_chat_history_collection():
    database = await get_database()
    return database.aichathistory

async def get_daily_challenges_collection():
    database = await get_database()
    return database.dailychallenges
