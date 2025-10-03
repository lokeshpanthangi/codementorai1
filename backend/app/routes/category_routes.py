"""
Category Routes
===============
API endpoints for category management
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.database import get_categories_collection
from app.models import CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories():
    """Get all active categories"""
    collection = await get_categories_collection()
    categories = await collection.find({"is_active": True}).sort("order", 1).to_list(None)
    
    # Convert ObjectId to string
    for cat in categories:
        cat["id"] = str(cat.pop("_id"))
    
    return categories

@router.get("/{slug}")
async def get_category_by_slug(slug: str):
    """Get a specific category by slug"""
    collection = await get_categories_collection()
    category = await collection.find_one({"slug": slug})
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category["id"] = str(category.pop("_id"))
    return category
