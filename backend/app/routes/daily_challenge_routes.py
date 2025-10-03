"""
Daily Challenge Routes
======================
API endpoints for daily challenges
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.database import get_daily_challenges_collection, get_problems_collection
from bson import ObjectId

router = APIRouter(prefix="/daily-challenge", tags=["Daily Challenge"])

@router.get("/today")
async def get_today_challenge():
    """Get today's daily challenge"""
    collection = await get_daily_challenges_collection()
    
    # Get today's date (start of day)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    challenge = await collection.find_one({"date": today})
    
    if not challenge:
        raise HTTPException(status_code=404, detail="No daily challenge for today")
    
    # Get problem details
    problems_collection = await get_problems_collection()
    problem = await problems_collection.find_one({"problem_number": challenge["problem_number"]})
    
    if problem:
        problem["id"] = str(problem.pop("_id"))
        challenge["problem"] = problem
    
    challenge["id"] = str(challenge.pop("_id"))
    return challenge

@router.get("/history")
async def get_challenge_history(limit: int = 7):
    """Get past daily challenges"""
    collection = await get_daily_challenges_collection()
    
    challenges = await collection.find().sort("date", -1).limit(limit).to_list(None)
    
    for challenge in challenges:
        challenge["id"] = str(challenge.pop("_id"))
    
    return challenges
