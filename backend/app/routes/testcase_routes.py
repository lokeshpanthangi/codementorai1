from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import TestCaseResponse
from app.database import get_testcases_collection
from bson import ObjectId

router = APIRouter(prefix="/testcases", tags=["Test Cases"])

@router.get("/{problem_number}/visible", response_model=List[TestCaseResponse])
async def get_visible_testcases(problem_number: int):
    """Get visible test cases for a problem (for Run button)"""
    testcases_collection = await get_testcases_collection()
    
    cursor = testcases_collection.find({
        "problem_number": problem_number,
        "is_hidden": False
    }).sort("test_case_number", 1)
    
    testcases = await cursor.to_list(length=100)
    
    return [
        TestCaseResponse(
            id=str(tc["_id"]),
            test_case_number=tc["test_case_number"],
            is_hidden=tc["is_hidden"],
            input_string=tc["input_string"],
            expected_output_string=tc["expected_output_string"],
            explanation=tc.get("explanation")
        )
        for tc in testcases
    ]

@router.get("/{problem_number}/hidden", response_model=List[TestCaseResponse])
async def get_hidden_testcases(problem_number: int):
    """Get hidden test cases for a problem (for Submit button - admin only in production)"""
    testcases_collection = await get_testcases_collection()
    
    cursor = testcases_collection.find({
        "problem_number": problem_number,
        "is_hidden": True
    }).sort("test_case_number", 1)
    
    testcases = await cursor.to_list(length=100)
    
    return [
        TestCaseResponse(
            id=str(tc["_id"]),
            test_case_number=tc["test_case_number"],
            is_hidden=tc["is_hidden"],
            input_string=tc["input_string"],
            expected_output_string=tc["expected_output_string"],
            explanation=tc.get("explanation")
        )
        for tc in testcases
    ]

@router.get("/{problem_number}/all", response_model=List[TestCaseResponse])
async def get_all_testcases(problem_number: int):
    """Get all test cases for a problem"""
    testcases_collection = await get_testcases_collection()
    
    cursor = testcases_collection.find({
        "problem_number": problem_number
    }).sort("test_case_number", 1)
    
    testcases = await cursor.to_list(length=100)
    
    return [
        TestCaseResponse(
            id=str(tc["_id"]),
            test_case_number=tc["test_case_number"],
            is_hidden=tc["is_hidden"],
            input_string=tc["input_string"],
            expected_output_string=tc["expected_output_string"],
            explanation=tc.get("explanation")
        )
        for tc in testcases
    ]
